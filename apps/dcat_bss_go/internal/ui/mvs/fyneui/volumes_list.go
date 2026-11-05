package fyneui

import (
	"dcat/internal/app/mvsapp"
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type VolumeRecord struct {
	Name string
}

type VolumesList struct {
	wList    *widget.List
	mvsApp   *mvsapp.MvsApp
	appState *AppState
}

func newVolumesList(mvsApp *mvsapp.MvsApp, appState *AppState) *VolumesList {

	vl := &VolumesList{
		mvsApp:   mvsApp,
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
		// fmt.Println("selected volume id: ", id)
		r := vl.appState.Volumes[id]
		err := vl.appState.OpenVolume(r.UUID)
		if err != nil {
			fmt.Println("ERROR: ", err)
		}
	}

	vl.wList = list

	// connect
	mvsApp.Connect(mvsapp.EvOpened, vl.onStorageOpened)

	return vl
}

func (vl *VolumesList) Widget() *fyne.Container {
	content := container.NewStack(vl.wList)
	return content
}

func (vl *VolumesList) onStorageOpened() error {

	vl.wList.Refresh()
	vl.wList.UnselectAll()

	return nil
}
