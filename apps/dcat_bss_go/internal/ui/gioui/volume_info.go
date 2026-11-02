package gioui

import (
	"dcat/internal/stor"
	"fmt"
	"time"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget/material"
)

type VolumeInfo struct {
	vp    *VolumeProvider
	units []KValue
}

func NewVolumeInfo(vp *VolumeProvider) *VolumeInfo {

	units := []KValue{
		NewKV("Name", func(vol *stor.Volume) string {
			return vol.Description.Name
		}),
		NewKV("ScanPath", func(vol *stor.Volume) string {
			return vol.Description.ScanPath
		}),
		NewKV("Created", func(vol *stor.Volume) string {
			return vol.Description.Created.Format(time.DateTime)
		}),
		NewKV("Icon", func(vol *stor.Volume) string {
			return fmt.Sprintf("%d", vol.Description.Icon)
		}),
		NewKV("Description", func(vol *stor.Volume) string {
			return vol.Description.Description
		}),
		NewKV("Records", func(vol *stor.Volume) string {
			return fmt.Sprintf("%d", len(vol.Records))
		}),
	}

	return &VolumeInfo{
		vp:    vp,
		units: units,
	}
}

/*
<title>
<row>
<row>
<row>
*/
func (vi *VolumeInfo) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	list := layout.List{
		Axis: layout.Vertical,
	}

	units := vi.units
	// backgroundColor := th.Bg
	return layout.Flex{Axis: layout.Vertical, Spacing: layout.SpaceEnd}.Layout(gtx,

		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			// paint.FillShape(gtx.Ops, backgroundColor, clipRectangle(gtx.Constraints.Max))
			return material.H6(th, "Volume").Layout(gtx)
		}),

		layout.Rigid(layout.Spacer{Width: unit.Dp(8)}.Layout), // Отступ между кнопками

		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			return layout.Inset{
				Top:    unit.Dp(6),
				Bottom: unit.Dp(6),
				Left:   unit.Dp(10),
			}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

				return list.Layout(gtx, len(units), func(gtx layout.Context, i int) layout.Dimensions {
					return units[i].Layout(th, gtx, vi.vp.Volume())
				})
			})
		}),
	)

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
	Key       string
	extractor func(*stor.Volume) string
}

func NewKV(label string, extractor func(*stor.Volume) string) KValue {
	return KValue{
		Key:       label,
		extractor: extractor,
	}
}

func (kv *KValue) Layout(th *material.Theme, gtx layout.Context, vol *stor.Volume) layout.Dimensions {
	mainLayout := layout.Flex{}

	value := kv.extractor(vol)
	return mainLayout.Layout(gtx,
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			return material.Body1(th, kv.Key).Layout(gtx)
		}),
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			return material.Body1(th, value).Layout(gtx)
		}),
	)
}
