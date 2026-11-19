package volumes

import (
	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Volumes struct {
	th *material.Theme

	listView *material.ListStyle
}

func NewVolumes(th *material.Theme) *Volumes {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)
	return &Volumes{
		th: th,

		listView: &listView,
	}
}

func (vms *Volumes) Layout(gtx C) D {
	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(vms.th, "Volumes frame").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// // Создаем стиль списка из темы, передавая указатель на состояние
			// listStyle := material.List(th, &fl.listState)

			// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
			// localFiles := fl.files

			// Вызываем макет
			return vms.listView.Layout(gtx, 100, func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					// return material.Body1(vms.th, "Volume row").Layout(gtx)
					return NewVolumeRow(vms.th).Layout(gtx)
				})
			})
		}),
	)

	// return material.Body1(mui.th, "Volumes frame").Layout(gtx)
}
