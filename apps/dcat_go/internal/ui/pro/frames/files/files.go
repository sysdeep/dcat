package files

import (
	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Files struct {
	th *material.Theme

	// listState *widget.List
	listView *material.ListStyle
}

func NewFiles(th *material.Theme) *Files {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)

	return &Files{
		th: th,
		// listState: &listState,
		listView: &listView,
	}
}

func (mui *Files) Layout(gtx C) D {
	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(mui.th, "Files frame").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// // Создаем стиль списка из темы, передавая указатель на состояние
			// listStyle := material.List(th, &fl.listState)

			// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
			// localFiles := fl.files

			// Вызываем макет
			return mui.listView.Layout(gtx, 100, func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					return material.Body1(mui.th, "File row").Layout(gtx)
				})
			})
		}),
	)

	// return material.Body1(mui.th, "Files frame").Layout(gtx)
}
