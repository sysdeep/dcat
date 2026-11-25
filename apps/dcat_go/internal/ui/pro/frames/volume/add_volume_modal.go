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
	"gioui.org/x/explorer"
)

const (
	ProcessingNone     = 0
	ProcessingStarted  = 1
	ProcessingFinished = 2
	ProcessingError    = 3
)

// TODO: валидация уникального имени
// TODO: валидация отсутствия имени

type AddVolumeModal struct {
	th  *material.Theme
	log *slog.Logger

	form     *EditVolumeForm
	closeBtn widget.Clickable
	saveBtn  widget.Clickable

	modalComponent *modal.Modal

	service VolumeService

	currentProcess         string
	currentProcessingState int
	processingError        atomic.Pointer[ProcessErrorMsg]
}

func NewAddVolumeModal(th *material.Theme, service VolumeService, ex *explorer.Explorer, log *slog.Logger) *AddVolumeModal {
	evm := AddVolumeModal{
		th:      th,
		log:     log,
		service: service,
		form:    NewEditVolumeForm(th, ex, log),
	}

	modalComponent := modal.NewModal(th, evm.headerLayout, evm.bodyLayout, evm.footerLayout, evm.onClose)
	evm.modalComponent = modalComponent

	return &evm

}

func (avm *AddVolumeModal) headerLayout(gtx layout.Context) layout.Dimensions {
	return material.H4(avm.th, "Добавление тома").Layout(gtx)
}

func (avm *AddVolumeModal) bodyLayout(gtx layout.Context) layout.Dimensions {
	return avm.form.Layout(gtx)
}

func (avm *AddVolumeModal) footerLayout(gtx layout.Context) layout.Dimensions {
	errMsg := ""
	if avm.processingError.Load() != nil {
		errMsg = avm.processingError.Load().Error.Error()
	}
	return layout.Flex{Axis: layout.Horizontal, Alignment: layout.Middle, Spacing: layout.SpaceStart, Gap: 10}.Layout(gtx,
		layout.Rigid(material.Body1(avm.th, errMsg).Layout),
		layout.Rigid(material.Body1(avm.th, avm.currentProcess).Layout),
		layout.Rigid(material.Button(avm.th, &avm.saveBtn, "Сканировать").Layout),
		layout.Rigid(material.Button(avm.th, &avm.closeBtn, "Закрыть").Layout),
	)
}

func (avm *AddVolumeModal) onClose() {
	avm.service.CloseVolumeModal()
}

func (avm *AddVolumeModal) Layout(gtx layout.Context) layout.Dimensions {

	switch avm.currentProcessingState {
	case ProcessingStarted:
		avm.currentProcess = "start"
	case ProcessingError:
		avm.currentProcess = "error"
	case ProcessingNone:
		avm.currentProcess = ""
	case ProcessingFinished:
		avm.currentProcess = "finished"
		avm.service.Refresh()
	}

	if avm.saveBtn.Clicked(gtx) {

		model := avm.form.GetModel()
		avm.startScanning(gtx, model)

	}

	if avm.closeBtn.Clicked(gtx) {
		avm.onClose()
		return layout.Dimensions{}
	}

	return avm.modalComponent.Layout(gtx)

}

func (avm *AddVolumeModal) startScanning(gtx layout.Context, vd proapp.VolumeDescription) {

	avm.currentProcessingState = ProcessingNone

	ch := make(chan interface{})

	go func() {
		for {
			msg := <-ch

			switch v := msg.(type) {
			case ProcessStartMsg:
				avm.currentProcessingState = ProcessingStarted
			case ProcessEndMsg:
				avm.currentProcessingState = ProcessingFinished
				close(ch)
				return
			case ProcessErrorMsg:
				avm.currentProcessingState = ProcessingError
				avm.processingError.Store(&v)
				close(ch)
				return
			}

			gtx.Execute(op.InvalidateCmd{})

		}
	}()

	go avm.service.MakeVolume(vd, ch)
}
