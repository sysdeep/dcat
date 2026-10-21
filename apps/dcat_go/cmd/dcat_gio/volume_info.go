package main

import (
	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget/material"
)

type VolumeInfo struct {
	units []*KValue
}

func NewVolumeInfo() *VolumeInfo {

	units := []*KValue{
		&KValue{Key: "path", Value: "/tmp"},
		&KValue{Key: "name", Value: "Tmp"},
		&KValue{Key: "icon"},
	}

	return &VolumeInfo{
		units: units,
	}
}

func (vi *VolumeInfo) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	list := layout.List{
		Axis: layout.Vertical,
	}

	return list.Layout(gtx, len(vi.units), func(gtx layout.Context, i int) layout.Dimensions {
		// return material.Label(th, unit.Sp(14.0), "123").Layout(gtx)
		return vi.units[i].Layout(th, gtx)
	})

	// return layout.Flex{}.Layout(gtx,
	// 	// We use weight 1 for both text and count to make them the same size.
	// 	layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
	// 		// We center align the text to the area available.
	// 		return layout.Center.Layout(gtx,
	// 			// Body1 is the default text size for reading.
	// 			material.Body1(th, "Files List").Layout)
	// 	}),
	// 	// We use an empty widget to add spacing between the text
	// 	// and the button.
	// 	layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
	// 	layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
	// 		// display the button.
	// 		// return material.Button(th, &counter.increase, "Count").Layout(gtx)
	// 		return material.Label(th, unit.Sp(100.0), "TExt").Layout(gtx)
	// 	}),
	// )
}

// =====================================================================
type KValue struct {
	Key   string
	Value string
}

func (kv *KValue) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {
	mainLayout := layout.Flex{}

	return mainLayout.Layout(gtx,
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			return material.Label(th, unit.Sp(14.0), kv.Key).Layout(gtx)
		}),
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(10, func(gtx layout.Context) layout.Dimensions {
			return material.Label(th, unit.Sp(14.0), kv.Value).Layout(gtx)
		}),
	)
}
