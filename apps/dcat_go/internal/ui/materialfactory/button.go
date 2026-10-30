package materialfactory

import (
	"gioui.org/widget"
	"gioui.org/widget/material"
)

func (m *MaterialFactory) Button(text string) material.ButtonStyle {
	cli := widget.Clickable{}
	btn := material.Button(m.th, &cli, text)
	return btn
}
