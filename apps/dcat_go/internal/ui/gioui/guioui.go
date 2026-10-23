package gioui

import (
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
)

var defaultMargin = unit.Dp(10)

type UI struct {
	theme *material.Theme

	// components
	mainLayout *layout.Flex
	ff         *FilesFrame
	vp         *VolumeProvider
	ip         *InfoPanel
}

// NewUI creates a new UI using the Go Fonts.
func NewUI(vp *VolumeProvider) *UI {
	ui := UI{
		theme:      material.NewTheme(),
		ff:         NewFilesFrame(vp),
		vp:         vp,
		ip:         NewInfoPanel(vp),
		mainLayout: &layout.Flex{},
	}
	ui.theme.Shaper = text.NewShaper(text.WithCollection(gofont.Collection()))
	return &ui
}

// Run handles window events and renders the application.
func (ui *UI) Run(w *app.Window) error {
	var ops op.Ops

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

// Layout displays the main program layout.
func (ui *UI) Layout(gtx layout.Context) layout.Dimensions {
	// inset is used to add padding around the window border.
	inset := layout.UniformInset(defaultMargin)
	return inset.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

		return ui.mainLayout.Layout(gtx,

			layout.Flexed(3, func(gtx layout.Context) layout.Dimensions {
				return ui.ff.Layout(ui.theme, gtx)
			}),
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				return ui.ip.Layout(ui.theme, gtx)
			}),
		)

	})
}
