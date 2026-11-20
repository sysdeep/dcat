package files

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

type FileRow struct {
	th       *material.Theme
	btnClick widget.Clickable
	fr       proapp.FileRecord
}

func NewFileRow(th *material.Theme, fr proapp.FileRecord) *FileRow {
	return &FileRow{
		th: th,
		fr: fr,
	}
}

func (vr *FileRow) Layout(gtx C) D {
	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	// if vr.btnClick.Clicked(gtx) && onClicked != nil {
	// 	onClicked(vr.fr)
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
				return material.Body1(vr.th, vr.fr.Name).Layout(gtx)
			}),
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		)

	})
}
