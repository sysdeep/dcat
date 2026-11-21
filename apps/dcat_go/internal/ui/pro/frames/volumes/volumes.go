package volumes

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"
	"image"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type C = layout.Context
type D = layout.Dimensions

var defaultMargin = unit.Dp(10)

type Volumes struct {
	th *material.Theme

	appState *appstate.AppState

	listView *material.ListStyle

	rowsBtn []widget.Clickable
}

func NewVolumes(th *material.Theme, appState *appstate.AppState) *Volumes {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)
	return &Volumes{
		th:       th,
		appState: appState,

		listView: &listView,
		rowsBtn:  make([]widget.Clickable, 0),
	}
}

func (vms *Volumes) Layout(gtx C) D {

	if len(vms.rowsBtn) < len(vms.appState.Volumes) {
		need := len(vms.appState.Volumes) - len(vms.rowsBtn)
		vms.rowsBtn = append(vms.rowsBtn, make([]widget.Clickable, need)...)
	}

	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(vms.th, "Volumes frame").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

			// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
			localVolumes := vms.appState.Volumes

			// Вызываем макет
			return vms.listView.Layout(gtx, len(localVolumes), func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

					if vms.rowsBtn[i].Clicked(gtx) {
						vms.onVolumeClicked(vms.appState.Volumes[i])
					}

					return vms.rowLayout(gtx, vms.appState.Volumes[i], &vms.rowsBtn[i])
				})
			})
		}),
	)

}

func (vms *Volumes) rowLayout(gtx C, vd proapp.VolumeDescription, btn *widget.Clickable) D {

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	// TODO
	icon := icons.FileAttachment
	// if kv.Data.FType == stor.FTYPE_DIR {
	// 	icon = icons.FileFolder
	// }

	// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
	return material.Clickable(gtx, btn, func(gtx layout.Context) layout.Dimensions {

		return mainLayout.Layout(gtx,
			// icon
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				size := 16
				gtx.Constraints = layout.Exact(image.Pt(size, size))
				ic, _ := widget.NewIcon(icon)
				return ic.Layout(gtx, vms.th.ContrastBg)
			}),
			// spacer
			layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
			// name
			layout.Flexed(2, func(gtx layout.Context) layout.Dimensions {
				// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
				return material.Body1(vms.th, vd.Name).Layout(gtx)
			}),
		)

	})
}

func (vms *Volumes) onVolumeClicked(vd proapp.VolumeDescription) {
	// TODO: error
	vms.appState.ReadVolume(vd)
}
