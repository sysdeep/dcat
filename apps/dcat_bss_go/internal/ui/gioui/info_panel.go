package gioui

import (
	"image/color"

	"gioui.org/layout"
	"gioui.org/op/paint"
	"gioui.org/unit"
	"gioui.org/widget/material"
)

type InfoPanel struct {
	vi *VolumeInfo
}

func NewInfoPanel(vp *VolumeProvider) *InfoPanel {
	return &InfoPanel{
		vi: NewVolumeInfo(vp),
	}
}

func (ip *InfoPanel) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	backgroundColor := color.NRGBA{R: 240, G: 240, B: 240, A: 255}

	return layout.Stack{}.Layout(gtx,
		// background
		layout.Expanded(func(gtx layout.Context) layout.Dimensions {
			paint.FillShape(gtx.Ops, backgroundColor, clipRectangle(gtx.Constraints.Max))
			return layout.Dimensions{Size: gtx.Constraints.Max}
		}),
		// Размещение кнопок внутри тулбара с отступами
		layout.Stacked(func(gtx layout.Context) layout.Dimensions {
			return layout.Inset{
				Top:    unit.Dp(6),
				Bottom: unit.Dp(6),
				Left:   unit.Dp(10),
			}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

				// Горизонтальный ряд для кнопок
				return layout.Flex{
					Axis:    layout.Vertical,
					Spacing: layout.SpaceEnd, // Кнопки прижаты к левому краю
				}.Layout(gtx,
					layout.Rigid(func(gtx layout.Context) layout.Dimensions {
						return ip.vi.Layout(th, gtx)
					}),
					// layout.Rigid(layout.Spacer{Height: unit.Dp(8)}.Layout), // Отступ между кнопками
					// layout.Rigid(func(gtx layout.Context) layout.Dimensions {
					// 	return ip.vi.Layout(th, gtx)
					// }),
					// layout.Rigid(layout.Spacer{Height: unit.Dp(8)}.Layout),
					// layout.Rigid(func(gtx layout.Context) layout.Dimensions {
					// 	return ip.vi.Layout(th, gtx)
					// }),
				)
			})
		}),
	)
}
