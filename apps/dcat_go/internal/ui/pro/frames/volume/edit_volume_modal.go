package volume

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/components/modal"
	"log/slog"
	"sync/atomic"

	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type EditVolumeModal struct {
	th  *material.Theme
	log *slog.Logger

	form     *EditVolumeForm
	closeBtn widget.Clickable
	saveBtn  widget.Clickable

	modalComponent *modal.Modal

	service   VolumeService
	initialVD proapp.VolumeDescription

	currentProcess         string
	currentProcessingState int
	processingError        atomic.Pointer[ProcessErrorMsg]
}

func NewEditVolumeModal(th *material.Theme, service VolumeService, vd proapp.VolumeDescription, log *slog.Logger) *EditVolumeModal {
	isNew := false
	evm := EditVolumeModal{
		th:        th,
		log:       log,
		service:   service,
		initialVD: vd,
		form:      NewEditVolumeForm(th, isNew, nil, vd, log),
	}

	modalComponent := modal.NewModal(th, evm.headerLayout, evm.bodyLayout, evm.footerLayout, evm.onClose)
	evm.modalComponent = modalComponent

	return &evm

}

func (evm *EditVolumeModal) headerLayout(gtx layout.Context) layout.Dimensions {
	return material.H4(evm.th, "Редактирование тома").Layout(gtx)
}

func (evm *EditVolumeModal) bodyLayout(gtx layout.Context) layout.Dimensions {
	return evm.form.Layout(gtx)
}

func (evm *EditVolumeModal) footerLayout(gtx layout.Context) layout.Dimensions {
	return layout.Flex{Axis: layout.Horizontal, Alignment: layout.Middle, Spacing: layout.SpaceStart, Gap: 10}.Layout(gtx,
		layout.Rigid(material.Button(evm.th, &evm.saveBtn, "Сохранить").Layout),
		layout.Rigid(material.Button(evm.th, &evm.closeBtn, "Закрыть").Layout),
	)
}

func (evm *EditVolumeModal) onClose() {
	evm.service.CloseVolumeModal()
}

func (evm *EditVolumeModal) Layout(gtx layout.Context) layout.Dimensions {

	// TODO
	switch evm.currentProcessingState {
	case ProcessingStarted:
		evm.currentProcess = "start"
	case ProcessingError:
		evm.currentProcess = "error"
	case ProcessingNone:
		evm.currentProcess = ""
	case ProcessingFinished:
		evm.currentProcess = "finished"
		evm.service.RefreshAndClose()
	}

	if evm.saveBtn.Clicked(gtx) {

		model := evm.form.GetModel()
		result := evm.initialVD
		result.Name = model.Name
		result.Description = model.Description
		result.Icon = model.Icon

		evm.startUpdating(gtx, result)

	}

	if evm.closeBtn.Clicked(gtx) {
		evm.onClose()
		return layout.Dimensions{}
	}

	return evm.modalComponent.Layout(gtx)

}

func (evm *EditVolumeModal) startUpdating(gtx layout.Context, vd proapp.VolumeDescription) {

	evm.currentProcessingState = ProcessingNone

	ch := make(chan interface{})

	go func() {
		for {
			msg := <-ch

			switch v := msg.(type) {
			case ProcessStartMsg:
				evm.currentProcessingState = ProcessingStarted
			case ProcessEndMsg:
				evm.currentProcessingState = ProcessingFinished
				close(ch)
				return
			case ProcessErrorMsg:
				evm.currentProcessingState = ProcessingError
				evm.processingError.Store(&v)
				close(ch)
				return
			}

			gtx.Execute(op.InvalidateCmd{})

		}
	}()

	go evm.service.UpdateVolume(vd, ch)
}
