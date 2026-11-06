package fyneui

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type VolumesList struct {
	wList    *widget.List
	appState *AppState
}

func newVolumesList(appState *AppState) *VolumesList {

	vl := &VolumesList{
		appState: appState,
	}

	list := widget.NewList(
		func() int {
			return len(appState.Volumes)
		},
		func() fyne.CanvasObject {
			i := widget.NewIcon(theme.FolderIcon())
			l := widget.NewLabel("template")
			return container.NewHBox(i, l)
		},
		func(i widget.ListItemID, o fyne.CanvasObject) {

			// 1. Приводим o к типу контейнера
			box := o.(*fyne.Container)

			// 2. Достаем Label (он на позиции 1 в HBox) и приводим к типу *widget.Label
			label := box.Objects[1].(*widget.Label)

			// 3. Обновляем текст
			label.SetText(appState.Volumes[i].Name)

			usedIcon := theme.FileIcon()
			// if fl.viewList[i].FType == stor.FTYPE_DIR {
			// 	usedIcon = theme.FolderIcon()
			// }
			icon := box.Objects[0].(*widget.Icon)
			icon.SetResource(usedIcon)

		})

	list.OnSelected = func(id widget.ListItemID) {
		r := vl.appState.Volumes[id]
		err := vl.appState.OpenVolume(r)
		if err != nil {
			// TODO: show error
			fmt.Println("ERROR: ", err)
		}
	}

	vl.wList = list

	// connect
	appState.Connect(AppStateVolumesChanged, vl.onVolumesChanged)

	return vl
}

func (vl *VolumesList) Widget() *fyne.Container {
	content := container.NewStack(vl.wList)
	return content
}

func (vl *VolumesList) onVolumesChanged() error {

	vl.wList.Refresh()
	vl.wList.UnselectAll()

	return nil
}
