package main

import (
	"dcat/internal/stor"
	"fmt"
	"image"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type FilesList struct {
	files     []*FileRecord
	vp        *VolumeProvider
	listState widget.List
	scrollbar widget.Scrollbar
}

func NewFileList(vp *VolumeProvider) *FilesList {
	files := []*FileRecord{
		&FileRecord{Name: "File 1", Size: 1024, IsDir: true},
		&FileRecord{Name: "File 2", Size: 1024},
		&FileRecord{Name: "File 3", Size: 1024},
		&FileRecord{Name: "File 4", Size: 1024},
	}

	rrs, _ := vp.GetRecords(1)
	for _, rr := range rrs {
		files = append(files, &FileRecord{Name: rr.Name, Size: int(rr.Size), IsDir: rr.FType == stor.FTYPE_DIR})
	}

	var listState widget.List
	listState.Axis = layout.Vertical

	return &FilesList{
		files:     files,
		vp:        vp,
		listState: listState,
	}
}

func (fl *FilesList) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	// Создаем стиль списка из темы, передавая указатель на состояние
	listStyle := material.List(th, &fl.listState)

	// Вызываем макет
	return listStyle.Layout(gtx, len(fl.files), func(gtx layout.Context, i int) layout.Dimensions {
		return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
			return fl.files[i].Layout(th, gtx)
		})
	})

}

// FileRecord -----------------------------------------------------------------

type FileRecord struct {
	Name  string
	IsDir bool
	Size  int

	click widget.Clickable
}

func (kv *FileRecord) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	if kv.click.Clicked(gtx) {
		// Здесь обрабатываем клик (например, открываем папку или файл)
		fmt.Printf("Кликнули по файлу: %s\n", kv.Name)
	}

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	icon := icons.FileCloudDone
	if kv.IsDir {
		icon = icons.FileFolder
	}

	// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
	return material.Clickable(gtx, &kv.click, func(gtx layout.Context) layout.Dimensions {

		return mainLayout.Layout(gtx,
			// icon
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				size := 16
				gtx.Constraints = layout.Exact(image.Pt(size, size))
				ic, _ := widget.NewIcon(icon)
				return ic.Layout(gtx, th.ContrastBg)
			}),
			layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
			// name
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
				return material.Body1(th, kv.Name).Layout(gtx)
			}),
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
			// size
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				return material.Body2(th, fmt.Sprintf("%d", kv.Size)).Layout(gtx)
			}),
		)

	})
}
