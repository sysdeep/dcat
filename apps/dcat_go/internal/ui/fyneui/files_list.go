package fyneui

import (
	"dcat/internal/stor"
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

type FilesList struct {
	list     *widget.List
	vp       *VolumeProvider
	viewList []stor.FileRecord
}

func NewFilesList(vp *VolumeProvider) *FilesList {
	// data := binding.BindStringList(
	// 	&[]string{"Item 1 foo bar zoo", "Item 2", "Item 3"},
	// )

	records, _ := vp.GetRecords(1) // TODO: error

	fl := FilesList{
		// list:     list,
		vp:       vp,
		viewList: records,
	}

	// data := []string{"Item 1 foo bar zoo", "Item 2", "Item 3"}

	list := widget.NewList(
		func() int {
			return len(fl.viewList)
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
			label.SetText(fl.viewList[i].Name)

			usedIcon := theme.FileIcon()
			if fl.viewList[i].FType == stor.FTYPE_DIR {
				usedIcon = theme.FolderIcon()
			}
			icon := box.Objects[0].(*widget.Icon)
			icon.SetResource(usedIcon)

		})

	list.OnSelected = func(id widget.ListItemID) {
		fmt.Println("selected index: ", id)
		r := fl.viewList[id]
		fmt.Println("selected id: ", r.ID)
		records, _ := vp.GetRecords(int(r.ID)) // TODO: error
		fmt.Println(records)
		fl.viewList = records
		list.Refresh()
		list.UnselectAll()
	}

	fl.list = list

	return &fl
}

func (vl *FilesList) Widget() *fyne.Container {

	btnHome := widget.NewButton("Home", func() {
		records, _ := vl.vp.GetRecords(0) // TODO: error
		vl.viewList = records
		vl.list.Refresh()
		vl.list.UnselectAll()
	})

	topBarContainer := container.NewHBox(btnHome)

	content := container.NewGridWithRows(2, topBarContainer, vl.list)

	// content := container.NewStack(topBarContainer, vl.list)
	return content
}
