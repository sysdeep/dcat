package modal

import (
	"image"
	"image/color"

	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/op/clip"
	"gioui.org/op/paint"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

var defaultSpacing = unit.Dp(12)
var dividerColor = color.NRGBA{R: 75, G: 75, B: 75, A: 50}

type CloseFunc func()

type Modal struct {
	th          *material.Theme
	backdropBtn widget.Clickable
	bodyBtn     widget.Clickable

	headerLayout layout.Widget
	bodyLayout   layout.Widget
	footerLayout layout.Widget

	onClose CloseFunc
}

func NewModal(
	th *material.Theme,
	headerLayout layout.Widget,
	bodyLayout layout.Widget,
	footerLayout layout.Widget,
	onClose CloseFunc,
) *Modal {
	m := Modal{
		th:           th,
		headerLayout: headerLayout,
		bodyLayout:   bodyLayout,
		footerLayout: footerLayout,
		onClose:      onClose,
	}

	return &m
}

func (modal *Modal) Layout(gtx layout.Context) layout.Dimensions {

	if modal.backdropBtn.Clicked(gtx) {
		modal.onClose()
		gtx.Execute(op.InvalidateCmd{})
	}

	return layout.Stack{Alignment: layout.Center}.Layout(gtx,

		// статическая подложка и пример модала
		layout.Expanded(func(gtx layout.Context) layout.Dimensions {

			return modal.backdropBtn.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
				background := color.NRGBA{R: 20, G: 20, B: 20, A: 150}
				paint.FillShape(gtx.Ops, background, clip.Rect{Max: gtx.Constraints.Max}.Op())
				return layout.Dimensions{Size: gtx.Constraints.Max}
			})

		}),

		// тело модала
		layout.Stacked(modal.modalLayout),
	)

}

func (modal *Modal) modalLayout(gtx layout.Context) layout.Dimensions {

	// TODO: можно задать в конструкторе константы типа MD LX и т.д.
	// Ограничиваем размеры модального окна
	orgConstraints := gtx.Constraints
	gtx.Constraints.Min = modal.reduceRect(orgConstraints.Max, 0.7)
	gtx.Constraints.Max = modal.reduceRect(orgConstraints.Max, 0.7)

	// NOTE: блокируем распространение кликов на подложку
	return modal.bodyBtn.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

		return layout.Background{}.Layout(gtx,
			// Фон (автоматически примет размер контента ниже)
			func(gtx layout.Context) layout.Dimensions {
				radius := 4
				defer clip.RRect{
					Rect: image.Rectangle{Max: gtx.Constraints.Min},
					NE:   radius, NW: radius, SE: radius, SW: radius,
				}.Push(gtx.Ops).Pop()
				paint.Fill(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255})
				return layout.Dimensions{Size: gtx.Constraints.Min}
			},
			// Контент поверх фона
			func(gtx layout.Context) layout.Dimensions {
				return layout.UniformInset(unit.Dp(16)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					return layout.Flex{
						Axis:      layout.Vertical,
						Alignment: layout.Middle,
					}.Layout(gtx,
						// header
						layout.Rigid(func(gtx layout.Context) layout.Dimensions {
							// return layout.UniformInset(defaultSpacing).Layout(gtx, modal.headerLayout)
							return modal.headerLayout(gtx)
						}),
						layout.Rigid(layout.Spacer{Height: defaultSpacing}.Layout),
						layout.Rigid(modal.horizontalDivider),
						layout.Rigid(layout.Spacer{Height: defaultSpacing}.Layout),

						// body
						layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
							return modal.bodyLayout(gtx)
						}),

						layout.Rigid(layout.Spacer{Height: defaultSpacing}.Layout),
						layout.Rigid(modal.horizontalDivider),
						layout.Rigid(layout.Spacer{Height: defaultSpacing}.Layout),

						// footer
						layout.Rigid(func(gtx layout.Context) layout.Dimensions {
							return modal.footerLayout(gtx)
						}),
					)
				})
			},
		)
	})

}

func (modal *Modal) reduceRect(p image.Point, factor float32) image.Point {
	return image.Point{
		X: int(float32(p.X) * factor),
		Y: int(float32(p.Y) * factor),
	}
}

func (modal *Modal) horizontalDivider(gtx layout.Context) layout.Dimensions {
	height := gtx.Dp(unit.Dp(1))
	size := image.Pt(gtx.Constraints.Max.X, height)

	paint.FillShape(gtx.Ops, dividerColor, clip.Rect{Max: size}.Op())
	return layout.Dimensions{Size: size}
}
