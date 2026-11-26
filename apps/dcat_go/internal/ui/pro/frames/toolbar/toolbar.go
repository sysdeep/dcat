package toolbar

import (
	"dcat/internal/ui/pro/appstate"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type C = layout.Context
type D = layout.Dimensions

type Toolbar struct {
	th       *material.Theme
	appState *appstate.AppState

	btnReadVolumes widget.Clickable
	btnAddVolume   widget.Clickable
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

	if tb.btnAddVolume.Clicked(gtx) {
		tb.appState.ShowAddVolumeModal()
	}

	// ic.Layout(gtx, tb.th.ContrastBg)

	return layout.Flex{Axis: layout.Horizontal, Gap: 8}.Layout(gtx,
		layout.Rigid(material.Body1(tb.th, "Toolbar frame").Layout),
		layout.Rigid(material.Button(tb.th, &tb.btnReadVolumes, "Read Volumes").Layout),
		layout.Rigid(material.Button(tb.th, &tb.btnAddVolume, "Add Volume").Layout),
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			// size := 16
			// gtx.Constraints = layout.Exact(image.Pt(size, size))
			ic, _ := widget.NewIcon(icons.AVAVTimer)
			return material.IconButton(tb.th, &tb.btnAddVolume, ic, "lalal").Layout(gtx)
		}),
	)
}
