package pro

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"
	"dcat/internal/ui/pro/frames/volume"
	"log/slog"

	"gioui.org/app"
	"gioui.org/font/gofont"
	"gioui.org/io/event"
	"gioui.org/io/key"
	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/op/clip"
	"gioui.org/text"
	"gioui.org/unit"
	"gioui.org/widget/material"
	"gioui.org/x/explorer"
)

var defaultMargin = unit.Dp(10)

type SecondaryLayout interface {
	Layout(gtx layout.Context) layout.Dimensions
}

type UI struct {
	w     *app.Window
	theme *material.Theme

	appState *appstate.AppState
	app      *proapp.App

	// components
	mainLayout *layout.Flex
	mainUI     *MainUI

	modals []SecondaryLayout

	log *slog.Logger

	expl *explorer.Explorer
}

func NewUI(w *app.Window, app *proapp.App, log *slog.Logger) *UI {
	th := material.NewTheme()
	th.Shaper = text.NewShaper(text.WithCollection(gofont.Collection()))

	ui := UI{
		theme:      th,
		mainLayout: &layout.Flex{},
		app:        app,
		log:        log,
		expl:       explorer.NewExplorer(w),
	}

	appState := appstate.NewAppState(app, &ui)
	ui.appState = appState
	ui.mainUI = newMainUI(th, appState)

	return &ui
}

// Run handles window events and renders the application.
func (ui *UI) Run(w *app.Window) error {
	var ops op.Ops

	// TODO: error
	// read the storage
	ui.appState.ReadVolumes()

	// Debug
	ui.ShowAddVolumeModal()

	// listen for events happening on the window.
	for {
		// detect the type of the event.
		switch e := w.Event().(type) {
		// this is sent when the application should re-render.
		case app.FrameEvent:
			// gtx is used to pass around rendering and event information.
			gtx := app.NewContext(&ops, e)

			// register a global key listener for the escape key wrapping our entire UI.
			area := clip.Rect{Max: gtx.Constraints.Max}.Push(gtx.Ops)
			event.Op(gtx.Ops, w)

			// check for presses of the escape key and close the window if we find them.
			for {
				event, ok := gtx.Event(key.Filter{
					Name: key.NameEscape,
				})
				if !ok {
					break
				}
				switch event := event.(type) {
				case key.Event:
					if event.Name == key.NameEscape {
						return nil
					}
				}
			}
			// render and handle UI.
			ui.Layout(gtx)
			area.Pop()
			// render and handle the operations from the UI.
			e.Frame(gtx.Ops)

		// this is sent when the application is closed.
		case app.DestroyEvent:
			return e.Err
		}
	}
}

func (ui *UI) Layout(gtx layout.Context) layout.Dimensions {

	// main layer
	var mms = make([]layout.StackChild, 0)
	mms = append(mms, layout.Stacked(ui.mainUI.Layout))

	// top layers
	for _, m := range ui.modals {
		mms = append(mms, layout.Stacked(m.Layout))
	}

	return layout.Stack{Alignment: layout.Center}.Layout(gtx,

		// main
		// layout.Stacked(ui.mainUI.Layout),
		// layout.Stacked(ui.volumeModal.Layout),
		mms...,
	)

}

func (ui *UI) ShowAddVolumeModal() {
	s := volume.NewVolumeService(ui.app, ui.HideModal)
	m := volume.NewAddVolumeModal(ui.theme, s, ui.expl, ui.log)
	ui.modals = append(ui.modals, m)
}

func (ui *UI) HideModal() {
	if len(ui.modals) > 0 {
		ui.modals = ui.modals[0 : len(ui.modals)-1]
	}
}
