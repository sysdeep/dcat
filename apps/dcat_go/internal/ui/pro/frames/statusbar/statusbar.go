package statusbar

import (
	"dcat/internal/ui/pro/appstate"
	"fmt"

	"gioui.org/layout"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Statusbar struct {
	th       *material.Theme
	appState *appstate.AppState
}

func NewStatusbar(th *material.Theme, appState *appstate.AppState) *Statusbar {
	return &Statusbar{
		th:       th,
		appState: appState,
	}
}

func (sbar *Statusbar) Layout(gtx C) D {

	storagePath := sbar.appState.GetStorageInfo()
	storageInfo := fmt.Sprintf("Storage: %s", storagePath)

	return layout.Flex{Axis: layout.Horizontal}.Layout(gtx,
		layout.Rigid(material.Body1(sbar.th, storageInfo).Layout),

		// TODO: version
		// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
		// 	return layout.Flex{Axis: layout.Horizontal, Alignment: layout.End}.Layout(gtx,
		// 		layout.Rigid(material.Body1(sbar.th, "v 0.0.1").Layout),
		// 	)
		// }),
	)
}
