package gioui

import (
	"image"
	"image/color"

	"gioui.org/layout"
	"gioui.org/op/paint"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type Modal struct {
	closeBtn widget.Clickable
}

func (m *Modal) Layout(th *material.Theme, gtx C) D {
	return layout.Center.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		// Ограничиваем размеры модального окна
		gtx.Constraints.Min = image.Point{X: gtx.Dp(300), Y: gtx.Dp(150)}
		gtx.Constraints.Max = image.Point{X: gtx.Dp(400), Y: gtx.Dp(300)}

		// Белый фон окна с закругленными углами
		return layout.UniformInset(unit.Dp(8)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
			// paint.FillShape(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255}, clip.RRect{
			// 	Rect: image.Rectangle{Max: gtx.Constraints.Min},
			// 	NE:   gtx.Dp(4), NW: gtx.Dp(4), SE: gtx.Dp(4), SW: gtx.Dp(4),
			// }.Op(gtx.Ops))

			paint.FillShape(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255}, clipRectangle(gtx.Constraints.Max))

			// Контент внутри модального окна
			return layout.UniformInset(unit.Dp(16)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
				return layout.Flex{
					Axis:      layout.Vertical,
					Alignment: layout.Middle,
					Spacing:   layout.SpaceBetween,
				}.Layout(gtx,
					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
						return material.H6(th, "Модальное окно").Layout(gtx)
					}),
					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
						return material.Body1(th, "Это простой пример поверх контента.").Layout(gtx)
					}),
					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
						return material.Button(th, &m.closeBtn, "Закрыть").Layout(gtx)
					}),
				)
			})
		})
	})
}
