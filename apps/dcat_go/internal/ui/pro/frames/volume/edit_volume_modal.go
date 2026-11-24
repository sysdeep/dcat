package volume

import (
	"dcat/internal/ui/pro/appstate"
	"dcat/internal/ui/pro/components/modal"
	"log/slog"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type EditVolumeModal struct {
	th       *material.Theme
	appState *appstate.AppState
	log      *slog.Logger

	form     *EditVolumeForm
	closeBtn widget.Clickable
	saveBtn  widget.Clickable

	modalComponent *modal.Modal
}

func NewEditVolumeModal(th *material.Theme, appState *appstate.AppState, log *slog.Logger) *EditVolumeModal {
	evm := EditVolumeModal{
		th:       th,
		appState: appState,
		log:      log,
		form:     NewEditVolumeForm(th, appState, log),
	}

	modalComponent := modal.NewModal(th, evm.headerLayout, evm.bodyLayout, evm.footerLayout, evm.onClose)
	evm.modalComponent = modalComponent

	return &evm

}

func (evm *EditVolumeModal) headerLayout(gtx layout.Context) layout.Dimensions {
	return material.H4(evm.th, "Добавление тома").Layout(gtx)
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
	evm.appState.CloseVolumeModal()
}

func (evm *EditVolumeModal) Layout(gtx layout.Context) layout.Dimensions {
	if evm.closeBtn.Clicked(gtx) {
		evm.onClose()
		return layout.Dimensions{}
	}

	return evm.modalComponent.Layout(gtx)

}
