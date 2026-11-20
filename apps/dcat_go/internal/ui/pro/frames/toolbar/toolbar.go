package toolbar

import (
	"dcat/internal/ui/pro/appstate"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Toolbar struct {
	th       *material.Theme
	appState *appstate.AppState

	btnReadVolumes widget.Clickable
}

func NewToolbar(th *material.Theme, appState *appstate.AppState) *Toolbar {
	return &Toolbar{
		th:       th,
		appState: appState,
	}
}

func (tb *Toolbar) Layout(gtx C) D {

	if tb.btnReadVolumes.Clicked(gtx) {
		// TODO: error
		tb.appState.ReadVolumes()
	}

	return layout.Flex{Axis: layout.Horizontal}.Layout(gtx,
		layout.Rigid(material.Body1(tb.th, "Toolbar frame").Layout),
		layout.Rigid(material.Button(tb.th, &tb.btnReadVolumes, "Read Volumes").Layout),
	)
}
