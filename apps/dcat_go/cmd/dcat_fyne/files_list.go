package main

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
)

type FilesList struct {
	list *widget.List
}

func NewFilesList() *FilesList {
	// data := binding.BindStringList(
	// 	&[]string{"Item 1 foo bar zoo", "Item 2", "Item 3"},
	// )

	data := []string{"Item 1 foo bar zoo", "Item 2", "Item 3"}

	list := widget.NewList(
		func() int {
			return len(data)
		},
		func() fyne.CanvasObject {
			// return
			// i := widget.NewIcon(theme.HomeIcon())
			// l := widget.NewLabel("template")
			// return container.NewHBox(i, l)
			// return widget.NewButtonWithIcon("template", theme.HomeIcon(), func() {})
			w := widget.NewTextGridFromString("aaa\nbbb")
			w.ShowLineNumbers = true
			w.SetCell(0, 0, widget.TextGridCell{Rune: 'v'})
			w.SetCell(5, 0, widget.TextGridCell{Rune: 'v'})
			return w
		},
		func(i widget.ListItemID, o fyne.CanvasObject) {
			// o.(*widget.Button).SetText(data[i])
			// o.(*fyne.Container).Objects[1].SetText(data[i])
			// o.(*widget.Label).Bind(i.(binding.String))

			// 1. Приводим o к типу контейнера
			// box := o.(*fyne.Container)

			// // 2. Достаем Label (он на позиции 1 в HBox) и приводим к типу *widget.Label
			// label := box.Objects[1].(*widget.Label)

			// // 3. Обновляем текст
			// label.SetText(data[i])

			// g := o.(*widget.TextGrid)
			// // g.Append()
			// g.SetText(data[i])
		})

	list.OnSelected = func(id widget.ListItemID) {
		fmt.Println(id)
	}

	return &FilesList{
		list: list,
	}
}

func (vl *FilesList) Widget() *widget.List {
	return vl.list
}
