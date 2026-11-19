package toolbar

import (
	"gioui.org/layout"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Toolbar struct {
	th *material.Theme
}

func NewToolbar(th *material.Theme) *Toolbar {
	return &Toolbar{
		th: th,
	}
}

func (mui *Toolbar) Layout(gtx C) D {
	return material.Body1(mui.th, "Toolbar frame").Layout(gtx)
}
