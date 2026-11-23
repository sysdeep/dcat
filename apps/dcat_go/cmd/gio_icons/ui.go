package main

import (
	"image"

	"gioui.org/app"
	"gioui.org/font/gofont"
	"gioui.org/io/event"
	"gioui.org/io/key"
	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/op/clip"
	"gioui.org/text"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

var defaultMargin = unit.Dp(10)

type UI struct {
	theme *material.Theme

	// components
	mainLayout *layout.Flex

	listState widget.List
}

func NewUI() *UI {
	th := material.NewTheme()
	th.Shaper = text.NewShaper(text.WithCollection(gofont.Collection()))

	ui := UI{
		theme:      th,
		mainLayout: &layout.Flex{},
	}

	ui.listState.Axis = layout.Vertical

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

	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H3(ui.theme, "Icons").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

			return material.List(ui.theme, &ui.listState).Layout(gtx, len(list), func(gtx layout.Context, i int) layout.Dimensions {
				return ui.rowLayout(gtx, list[i])
			})
		}),
	)

}

func (ui *UI) rowLayout(gtx layout.Context, iconData IconData) layout.Dimensions {
	return layout.Flex{Axis: layout.Horizontal, Alignment: layout.Middle}.Layout(gtx,
		// icon
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			size := 32
			gtx.Constraints = layout.Exact(image.Pt(size, size))
			ic, _ := widget.NewIcon(iconData.data)
			return ic.Layout(gtx, ui.theme.ContrastBg)
		}),
		layout.Rigid(layout.Spacer{Width: unit.Dp(16)}.Layout),
		// name
		layout.Rigid(material.Body1(ui.theme, iconData.name).Layout),
	)

}
