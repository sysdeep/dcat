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
	"gioui.org/widget"
	"gioui.org/widget/material"
)

var defaultMargin = unit.Dp(10)

type UI struct {
	theme *material.Theme

	appState *appstate.AppState

	// components
	mainLayout *layout.Flex
	mainUI     *MainUI

	// modal
	volumeModal     *volume.EditVolumeModal
	showVolumeModal bool
	backdropBtn     widget.Clickable
	// ff         *FilesFrame
	// vp         *state.VolumeProvider
	// ip         *InfoPanel

	// example
	// showModal  bool
	// scrimClick widget.Clickable
	// closeBtn   widget.Clickable
	// openBtn    widget.Clickable
	// modal      *Modal
}

func NewUI(app *proapp.App, log *slog.Logger) *UI {
	th := material.NewTheme()
	th.Shaper = text.NewShaper(text.WithCollection(gofont.Collection()))

	appState := appstate.NewAppState(app)
	ui := UI{
		theme:           th,
		appState:        appState,
		mainLayout:      &layout.Flex{},
		mainUI:          newMainUI(th, appState),
		volumeModal:     volume.NewEditVolumeModal(th, appState, log),
		showVolumeModal: true,
	}

	return &ui
}

// Run handles window events and renders the application.
func (ui *UI) Run(w *app.Window) error {
	var ops op.Ops

	// TODO: error
	// read the storage
	ui.appState.ReadVolumes()

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

	// // Открытие модального окна
	// if ui.openBtn.Clicked(gtx) {
	// 	ui.showModal = true
	// }
	// // Закрытие модального окна по кнопке или клику вне его
	// if ui.closeBtn.Clicked(gtx) || ui.scrimClick.Clicked(gtx) {
	// 	ui.showModal = false
	// }

	// Обрабатываем клик по фону (если нужно закрывать окно)
	if ui.backdropBtn.Clicked(gtx) {
		ui.showVolumeModal = false
	}

	return layout.Stack{Alignment: layout.Center}.Layout(gtx,

		// main
		layout.Stacked(ui.mainUI.Layout),
		layout.Stacked(ui.volumeModal.Layout),
		// статическая подложка и пример модала
		// layout.Expanded(func(gtx C) D {

		// 	return ui.backdropBtn.Layout(gtx, func(gtx C) D {
		// 		background := color.NRGBA{R: 20, G: 20, B: 20, A: 150}
		// 		paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
		// 		return layout.Dimensions{Size: gtx.Constraints.Max}
		// 	})

		// 	// background := color.NRGBA{R: 20, G: 20, B: 20, A: 150} // Полупрозрачный черный
		// 	// paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
		// 	// return layout.Dimensions{Size: gtx.Constraints.Max}
		// }),
		// // layout.Expanded(ui.volumeForm.Layout),
		// layout.Stacked(func(gtx layout.Context) layout.Dimensions {
		// 	// 	// TODO: is modal
		// 	if ui.showVolumeModal == false {
		// 		return layout.Dimensions{}
		// 	}

		// 	return ui.volumeModal.Layout(gtx)

		// 	// 	return layout.Center.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		// 	// 		gtx.Constraints.Min = image.Point{}
		// 	// 		gtx.Constraints.Max = image.Point{X: gtx.Dp(400), Y: gtx.Dp(300)}
		// 	// 		return ui.volumeModal.Layout(gtx)
		// 	// 	})

		// 	// 	// return layout.Stack{}.Layout(gtx,
		// 	// 	// 	// layout.Expanded(func(gtx layout.Context) layout.Dimensions {
		// 	// 	// 	// 	// Кнопка на весь экран для обработки клика "мимо окна"
		// 	// 	// 	// 	return material.Clickable(gtx, &ui.scrimClick, func(gtx layout.Context) layout.Dimensions {
		// 	// 	// 	// 		background := color.NRGBA{R: 0, G: 0, B: 0, A: 150} // Полупрозрачный черный
		// 	// 	// 	// 		paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
		// 	// 	// 	// 		return layout.Dimensions{Size: gtx.Constraints.Max}
		// 	// 	// 	// 	})
		// 	// 	// 	// }),
		// 	// 	// 	// Центрирование самого тела модального окна
		// 	// 	// 	layout.Expanded(func(gtx layout.Context) layout.Dimensions {
		// 	// 	// 		return ui.volumeModal.Layout(gtx)
		// 	// 	// 		// return layout.Center.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		// 	// 	// 		// 	return ui.volumeModal.Layout(gtx)
		// 	// 	// 		// })
		// 	// 	// 	}),
		// 	// 	// )
		// }),
		// // layout.Stacked(func(gtx layout.Context) layout.Dimensions {

		// // 	// inset is used to add padding around the window border.
		// // 	inset := layout.UniformInset(defaultMargin)
		// // 	return inset.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

		// // 		return ui.mainLayout.Layout(gtx,

		// // 			layout.Flexed(3, func(gtx layout.Context) layout.Dimensions {
		// // 				return ui.ff.Layout(ui.theme, gtx)
		// // 			}),
		// // 			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
		// // 				return ui.ip.Layout(ui.theme, gtx)
		// // 			}),
		// // 			// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
		// // 			// 	return material.Button(ui.theme, &ui.openBtn, "open").Layout(gtx)
		// // 			// }),
		// // 			// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
		// // 			// 	return ui.modal.Layout(ui.theme, gtx)
		// // 			// }),
		// // 		)

		// // 	})

		// // }),

	)

}
