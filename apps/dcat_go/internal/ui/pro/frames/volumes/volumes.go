package volumes

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Volumes struct {
	th *material.Theme

	appState *appstate.AppState

	listView *material.ListStyle

	vrs []*VolumeRow
}

func NewVolumes(th *material.Theme, appState *appstate.AppState) *Volumes {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)
	return &Volumes{
		th:       th,
		appState: appState,

		listView: &listView,
		vrs:      make([]*VolumeRow, 0),
	}
}

func (vms *Volumes) Layout(gtx C) D {
	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(vms.th, "Volumes frame").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

			// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
			localVolumes := vms.appState.Volumes
			vms.vrs = make([]*VolumeRow, 0)

			// Вызываем макет
			return vms.listView.Layout(gtx, len(localVolumes), func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					vr := NewVolumeRow(vms.th, localVolumes[i])
					vms.vrs = append(vms.vrs, vr)
					return vr.Layout(gtx, vms.onVolumeClicked)
				})
			})
		}),
	)

}

func (vms *Volumes) onVolumeClicked(vd proapp.VolumeDescription) {
	// TODO: error
	vms.appState.ReadVolume(vd)
}
