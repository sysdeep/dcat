package volumes

import (
	"dcat/internal/app/proapp"
	"image"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

var defaultMargin = unit.Dp(10)

type VolumeRow struct {
	th       *material.Theme
	btnClick widget.Clickable
	vd       proapp.VolumeDescription
}

func NewVolumeRow(th *material.Theme, vd proapp.VolumeDescription) *VolumeRow {
	return &VolumeRow{
		th: th,
		vd: vd,
	}
}

func (vr *VolumeRow) Layout(gtx C, onClicked func(proapp.VolumeDescription)) D {
	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	// if vr.btnClick.Clicked(gtx) {
	// 	// onClicked(vr.vd)
	// 	fmt.Println("volume clicked")
	// }

	// if vr.btnClick.Clicked(gtx) && onClicked != nil {
	// 	// onClicked(vr.vd)
	// 	fmt.Println("volume clicked")
	// }

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	icon := icons.FileAttachment
	// if kv.Data.FType == stor.FTYPE_DIR {
	// 	icon = icons.FileFolder
	// }

	// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
	return material.Clickable(gtx, &vr.btnClick, func(gtx layout.Context) layout.Dimensions {

		return mainLayout.Layout(gtx,
			// icon
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				size := 16
				gtx.Constraints = layout.Exact(image.Pt(size, size))
				ic, _ := widget.NewIcon(icon)
				return ic.Layout(gtx, vr.th.ContrastBg)
			}),
			// spacer
			layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
			// name
			layout.Flexed(2, func(gtx layout.Context) layout.Dimensions {
				// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
				return material.Body1(vr.th, vr.vd.Name).Layout(gtx)
			}),
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				return material.Body2(vr.th, "foo").Layout(gtx)
			}),
		)

	})
}
