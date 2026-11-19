package statusbar

import (
	"gioui.org/layout"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Statusbar struct {
	th *material.Theme
}

func NewStatusbar(th *material.Theme) *Statusbar {
	return &Statusbar{
		th: th,
	}
}

func (sbar *Statusbar) Layout(gtx C) D {
	return material.Body1(sbar.th, "Statusbar frame").Layout(gtx)
}
