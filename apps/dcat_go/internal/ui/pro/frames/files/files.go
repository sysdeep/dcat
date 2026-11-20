package files

import (
	"dcat/internal/ui/pro/appstate"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

type Files struct {
	th       *material.Theme
	appState *appstate.AppState

	// listState *widget.List
	listView *material.ListStyle
}

func NewFiles(th *material.Theme, appState *appstate.AppState) *Files {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)

	return &Files{
		th:       th,
		appState: appState,
		listView: &listView,
	}
}

func (fls *Files) Layout(gtx C) D {
	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(fls.th, "Files frame").Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// // Создаем стиль списка из темы, передавая указатель на состояние
			// listStyle := material.List(th, &fl.listState)
			if fls.appState.CurrentVolume == nil {
				return layout.Dimensions{}
			}

			// TODO: folder records
			// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
			localFiles := fls.appState.CurrentVolume.Records

			// Вызываем макет
			return fls.listView.Layout(gtx, len(localFiles), func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					return NewFileRow(fls.th, localFiles[i]).Layout(gtx)
				})
			})
		}),
	)

	// return material.Body1(mui.th, "Files frame").Layout(gtx)
}
