package main

import (
	"dcat/internal/stor"
	"log"
	"os"
	"strconv"

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

func main() {

	// dataset
	vv, err := stor.Read("/tmp/db1")
	if err != nil {
		panic(err)
	}

	vp := NewVolumeProvider(vv)

	ui := NewUI(vp)

	// This creates a new application window and starts the UI.
	go func() {
		w := new(app.Window)
		w.Option(
			app.Title("Counter"),
			app.Size(unit.Dp(240), unit.Dp(70)),
		)
		if err := ui.Run(w); err != nil {
			log.Println(err)
			os.Exit(1)
		}
		os.Exit(0)
	}()

	// This starts Gio main.
	app.Main()

}

var defaultMargin = unit.Dp(10)

type UI struct {
	// Theme is used to hold the fonts used throughout the application.
	Theme *material.Theme

	// Counter displays and keeps the state of the counter.
	Counter Counter
	vi      *VolumeInfo
	ff      *FilesFrame
	vp      *VolumeProvider
}

// NewUI creates a new UI using the Go Fonts.
func NewUI(vp *VolumeProvider) *UI {
	ui := &UI{
		vi: NewVolumeInfo(),
		ff: NewFilesFrame(vp),
		vp: vp,
	}
	ui.Theme = material.NewTheme()
	ui.Theme.Shaper = text.NewShaper(text.WithCollection(gofont.Collection()))
	return ui
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

		mainLayout := layout.Flex{}

		return mainLayout.Layout(gtx,
			// // We use weight 1 for both text and count to make them the same size.
			// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// 	// We center align the text to the area available.
			// 	return ui.Counter.Layout(ui.Theme, gtx)
			// }),
			// // We use an empty widget to add spacing between the text
			// // and the button.
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
			layout.Flexed(3, func(gtx layout.Context) layout.Dimensions {
				// display the button.
				return ui.ff.Layout(ui.Theme, gtx)
			}),
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				// display the button.
				return ui.vi.Layout(ui.Theme, gtx)
			}),
		)

		// return ui.Counter.Layout(ui.Theme, gtx)
	})
}

// ==============================================================================
// Counter is a component that keeps track of it's state and
// displays itself as a label and a button.
type Counter struct {
	// Count is the current value.
	Count int

	// increase is used to track button clicks.
	increase widget.Clickable
}

// Layout lays out the counter and handles input.
func (counter *Counter) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {
	// first, update the count so that once it renders it has the correct value
	counter.UpdateCount(gtx)

	// Flex layout lays out widgets from left to right by default.
	return layout.Flex{}.Layout(gtx,
		// We use weight 1 for both text and count to make them the same size.
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// We center align the text to the area available.
			return layout.Center.Layout(gtx,
				// Body1 is the default text size for reading.
				material.Body1(th, strconv.Itoa(counter.Count)).Layout)
		}),
		// We use an empty widget to add spacing between the text
		// and the button.
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// display the button.
			return material.Button(th, &counter.increase, "Count").Layout(gtx)
		}),
	)
}

func (counter *Counter) UpdateCount(gtx layout.Context) {
	// For every click on the button increment the count.
	for counter.increase.Clicked(gtx) {
		counter.Count++
	}
}

// ========================================================
