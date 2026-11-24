// package volume

// import (
// 	"dcat/internal/ui/pro/appstate"
// 	"image"
// 	"image/color"
// 	"log/slog"

// 	"gioui.org/layout"
// 	"gioui.org/op/clip"
// 	"gioui.org/op/paint"
// 	"gioui.org/unit"
// 	"gioui.org/widget"
// 	"gioui.org/widget/material"
// )

// type EditVolumeModal struct {
// 	th       *material.Theme
// 	appState *appstate.AppState
// 	log      *slog.Logger

// 	backdropBtn widget.Clickable
// 	form        *EditVolumeForm
// }

// func NewEditVolumeModal(th *material.Theme, appState *appstate.AppState, log *slog.Logger) *EditVolumeModal {
// 	return &EditVolumeModal{
// 		th:       th,
// 		appState: appState,
// 		log:      log,
// 		form:     NewEditVolumeForm(th, appState, log),
// 	}
// }

// func (evm *EditVolumeModal) Layout(gtx layout.Context) layout.Dimensions {
// 	if evm.appState.ISEditModal == false {
// 		return layout.Dimensions{}
// 	}

// 	if evm.backdropBtn.Clicked(gtx) {
// 		evm.appState.CloseVolumeModal()
// 	}

// 	return layout.Stack{Alignment: layout.Center}.Layout(gtx,

// 		// main
// 		// layout.Stacked(ui.mainUI.Layout),
// 		// статическая подложка и пример модала
// 		layout.Expanded(func(gtx layout.Context) layout.Dimensions {

// 			return evm.backdropBtn.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
// 				background := color.NRGBA{R: 20, G: 20, B: 20, A: 150}
// 				paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
// 				return layout.Dimensions{Size: gtx.Constraints.Max}
// 			})

// 			// background := color.NRGBA{R: 20, G: 20, B: 20, A: 150} // Полупрозрачный черный
// 			// paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
// 			// return layout.Dimensions{Size: gtx.Constraints.Max}
// 		}),

// 		// тело модала
// 		layout.Stacked(evm.modalLayout),
// 	)
// }

// func (evm *EditVolumeModal) modalLayout(gtx layout.Context) layout.Dimensions {

// 	// TODO: можно задать в конструкторе константы типа MD LX и т.д.
// 	// Ограничиваем размеры модального окна
// 	orgConstraints := gtx.Constraints
// 	gtx.Constraints.Min = evm.reduceRect(orgConstraints.Max, 0.7)
// 	gtx.Constraints.Max = evm.reduceRect(orgConstraints.Max, 0.7)

// 	return layout.Background{}.Layout(gtx,
// 		// Фон (автоматически примет размер контента ниже)
// 		func(gtx layout.Context) layout.Dimensions {
// 			radius := 4
// 			defer clip.RRect{
// 				Rect: image.Rectangle{Max: gtx.Constraints.Min},
// 				NE:   radius, NW: radius, SE: radius, SW: radius,
// 			}.Push(gtx.Ops).Pop()
// 			paint.Fill(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255})
// 			return layout.Dimensions{Size: gtx.Constraints.Min}
// 		},
// 		// Контент поверх фона
// 		func(gtx layout.Context) layout.Dimensions {
// 			return layout.UniformInset(unit.Dp(16)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
// 				return layout.Flex{
// 					Axis:      layout.Vertical,
// 					Alignment: layout.Middle,
// 				}.Layout(gtx,
// 					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
// 						return material.H6(evm.th, "Модальное окно").Layout(gtx)
// 					}),
// 					layout.Rigid(layout.Spacer{Height: unit.Dp(12)}.Layout),
// 					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
// 						return material.Body1(evm.th, "Это простой пример поверх контента.").Layout(gtx)
// 					}),
// 					layout.Rigid(layout.Spacer{Height: unit.Dp(12)}.Layout),
// 					layout.Flexed(1, evm.form.Layout),
// 					layout.Rigid(layout.Spacer{Height: unit.Dp(12)}.Layout),
// 					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
// 						return material.Button(evm.th, &evm.backdropBtn, "Закрыть").Layout(gtx)
// 					}),
// 				)
// 			})
// 		},
// 	)
// }

// func (evm *EditVolumeModal) reduceRect(p image.Point, factor float32) image.Point {
// 	return image.Point{
// 		X: int(float32(p.X) * factor),
// 		Y: int(float32(p.Y) * factor),
// 	}
// }

// // NOTE: wrk variant
// // func (evm *EditVolumeModal) Layout(gtx layout.Context) layout.Dimensions {
// // 	// Ограничиваем размеры модального окна
// // 	gtx.Constraints.Min = image.Point{X: gtx.Dp(300), Y: gtx.Dp(150)}
// // 	gtx.Constraints.Max = image.Point{X: gtx.Dp(400), Y: gtx.Dp(300)}

// // 	return layout.Background{}.Layout(gtx,
// // 		// Фон (автоматически примет размер контента ниже)
// // 		func(gtx layout.Context) layout.Dimensions {
// // 			defer clip.RRect{
// // 				Rect: image.Rectangle{Max: gtx.Constraints.Min},
// // 				NE:   gtx.Dp(4), NW: gtx.Dp(4), SE: gtx.Dp(4), SW: gtx.Dp(4),
// // 			}.Push(gtx.Ops).Pop()
// // 			paint.Fill(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255})
// // 			return layout.Dimensions{Size: gtx.Constraints.Min}
// // 		},
// // 		// Контент поверх фона
// // 		func(gtx layout.Context) layout.Dimensions {
// // 			return layout.UniformInset(unit.Dp(16)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
// // 				return layout.Flex{
// // 					Axis:      layout.Vertical,
// // 					Alignment: layout.Middle,
// // 				}.Layout(gtx,
// // 					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
// // 						return material.H6(evm.th, "Модальное окно").Layout(gtx)
// // 					}),
// // 					layout.Rigid(layout.Spacer{Height: unit.Dp(12)}.Layout),
// // 					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
// // 						return material.Body1(evm.th, "Это простой пример поверх контента.").Layout(gtx)
// // 					}),
// // 				)
// // 			})
// // 		},
// // 	)
// // }
