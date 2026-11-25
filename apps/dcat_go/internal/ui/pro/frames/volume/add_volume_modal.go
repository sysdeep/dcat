package volume

import (
	"dcat/internal/ui/pro/components/modal"
	"fmt"
	"log/slog"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"gioui.org/x/explorer"
)

type AddVolumeModal struct {
	th  *material.Theme
	log *slog.Logger

	form     *EditVolumeForm
	closeBtn widget.Clickable
	saveBtn  widget.Clickable

	modalComponent *modal.Modal

	evs VolumeService
}

func NewAddVolumeModal(th *material.Theme, evs VolumeService, ex *explorer.Explorer, log *slog.Logger) *AddVolumeModal {
	evm := AddVolumeModal{
		th:   th,
		log:  log,
		evs:  evs,
		form: NewEditVolumeForm(th, ex, log),
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
	return layout.Flex{Axis: layout.Horizontal, Alignment: layout.Middle, Spacing: layout.SpaceStart, Gap: 10}.Layout(gtx,
		layout.Rigid(material.Button(avm.th, &avm.saveBtn, "Сохранить").Layout),
		layout.Rigid(material.Button(avm.th, &avm.closeBtn, "Закрыть").Layout),
	)
}

func (avm *AddVolumeModal) onClose() {
	avm.evs.CloseVolumeModal()
}

func (avm *AddVolumeModal) Layout(gtx layout.Context) layout.Dimensions {

	if avm.saveBtn.Clicked(gtx) {

		model := avm.form.GetModel()
		fmt.Println(model)

		go avm.evs.MakeVolume(model)

	}

	if avm.closeBtn.Clicked(gtx) {
		avm.onClose()
		return layout.Dimensions{}
	}

	return avm.modalComponent.Layout(gtx)

}
