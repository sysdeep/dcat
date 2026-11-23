package volume

import (
	"dcat/internal/ui/pro/appstate"
	"log/slog"

	"gioui.org/layout"
	"gioui.org/widget/material"
)

type EditVolumeForm struct {
	th       *material.Theme
	appState *appstate.AppState
	log      *slog.Logger
}

func NewEditVolumeForm(th *material.Theme, appState *appstate.AppState, log *slog.Logger) *EditVolumeForm {
	return &EditVolumeForm{
		th:       th,
		appState: appState,
		log:      log,
	}
}

func (ev *EditVolumeForm) Layout(gtx layout.Context) layout.Dimensions {
	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H3(ev.th, "Volume").Layout),
		layout.Flexed(10, material.H6(ev.th, "body").Layout),
	)
}
