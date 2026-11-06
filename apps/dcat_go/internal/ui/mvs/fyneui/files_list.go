package fyneui

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type FilesList struct {
	list     *widget.List
	appState *AppState
}

func NewFilesList(appState *AppState) *FilesList {

	fl := FilesList{
		appState: appState,
	}

	list := widget.NewList(
		func() int {
			return len(appState.Files.Get())
		},
		func() fyne.CanvasObject {
			wIcon := widget.NewIcon(theme.FolderIcon())
			wName := widget.NewLabel("template")
			wSize := widget.NewLabel("size")
			return container.NewHBox(wIcon, wName, wSize)
		},
		func(i widget.ListItemID, o fyne.CanvasObject) {

			record := appState.Files.Get()[i]

			box := o.(*fyne.Container)

			labelName := box.Objects[1].(*widget.Label)
			labelName.SetText(record.Name)

			usedIcon := theme.FileIcon()
			if record.IsFolder() {
				usedIcon = theme.FolderIcon()
			}
			icon := box.Objects[0].(*widget.Icon)
			icon.SetResource(usedIcon)

			sizeLabel := box.Objects[2].(*widget.Label)
			sizeLabel.SetText(fmt.Sprintf("%d bytes", 0))

		})

	list.OnSelected = func(id widget.ListItemID) {
		record := appState.Files.Get()[id]
		if record.IsFolder() {
			appState.OpenFolder(record)
		}
	}

	fl.list = list

	// connect
	appState.Files.Connect(fl.onFilesUpdated)

	return &fl
}

func (vl *FilesList) Widget() *fyne.Container {

	content := container.NewStack(vl.list)
	return content
}

func (fl *FilesList) onFilesUpdated() {
	fl.list.Refresh()
	fl.list.UnselectAll()
}
