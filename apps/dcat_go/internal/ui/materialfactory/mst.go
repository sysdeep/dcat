package materialfactory

import (
	"gioui.org/widget/material"
)

// MaterialFactory - фабрика stateFull виджетов
type MaterialFactory struct {
	th *material.Theme
}

func NewMaterialFactory(th *material.Theme) *MaterialFactory {
	return &MaterialFactory{
		th: th,
	}
}

func (mf *MaterialFactory) Theme() *material.Theme {
	return mf.th
}
