package gioui

import (
	"image/color"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type OpenPanel struct {
	th      *material.Theme
	editor  widget.Editor
	openBtn widget.Clickable
}

func NewOpenPanel(th *material.Theme) *OpenPanel {
	return &OpenPanel{
		th: th,
	}
}

func (op *OpenPanel) Layout(gtx layout.Context) layout.Dimensions {
	ed := material.Editor(op.th, &op.editor, "volume path")
	border := widget.Border{
		Color:        color.NRGBA{R: 204, G: 204, B: 204, A: 255},
		CornerRadius: unit.Dp(1),
		Width:        unit.Dp(1),
	}
	margins := layout.UniformInset(unit.Dp(9))

	return layout.Flex{
		Axis:    layout.Horizontal,
		Spacing: layout.SpaceEnd,
	}.Layout(gtx,
		layout.Rigid(func(gtx C) D {
			return border.Layout(gtx, func(gtx C) D {
				return margins.Layout(gtx, ed.Layout)
			})
		}),
		layout.Rigid(layout.Spacer{Width: unit.Dp(8)}.Layout),
		layout.Rigid(material.Button(op.th, &op.openBtn, "Open").Layout),
	)
}
