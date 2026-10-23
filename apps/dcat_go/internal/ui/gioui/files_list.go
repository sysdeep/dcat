package gioui

import (
	"dcat/internal/stor"
	"fmt"
	"image"
	"slices"
	"strings"
	"time"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"github.com/samber/lo"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type FilesList struct {
	files     []FileRecord
	vp        *VolumeProvider
	listState widget.List
	scrollbar widget.Scrollbar
}

func NewFileList(vp *VolumeProvider) *FilesList {
	files := []FileRecord{
		// &FileRecord{Name: "File 1", Size: 1024, IsDir: true},
		// &FileRecord{Name: "File 2", Size: 1024},
		// &FileRecord{Name: "File 3", Size: 1024},
		// &FileRecord{Name: "File 4", Size: 1024},
	}

	// rrs, _ := vp.GetRecords(0)
	// for _, rr := range rrs {
	// 	files = append(files, &FileRecord{Name: rr.Name, Size: int(rr.Size), IsDir: rr.FType == stor.FTYPE_DIR})
	// }

	var listState widget.List
	listState.Axis = layout.Vertical

	fl := FilesList{
		files:     files,
		vp:        vp,
		listState: listState,
	}

	vp.ConnectHandler(fl.onUpdate)
	fl.onUpdate()

	return &fl
}

func (fl *FilesList) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	// Создаем стиль списка из темы, передавая указатель на состояние
	listStyle := material.List(th, &fl.listState)

	// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
	localFiles := fl.files

	// Вызываем макет
	return listStyle.Layout(gtx, len(localFiles), func(gtx layout.Context, i int) layout.Dimensions {
		return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
			return localFiles[i].Layout(th, gtx, fl.onClicked)
		})
	})

}

func (fl *FilesList) onUpdate() error {

	files := []FileRecord{}
	rrs, _ := fl.vp.GetActualRecords()

	rDirs := lo.Filter(rrs, func(f stor.FileRecord, i int) bool {
		return f.FType == stor.FTYPE_DIR
	})

	rFiles := lo.Filter(rrs, func(f stor.FileRecord, i int) bool {
		return f.FType == stor.FTYPE_FILE
	})

	oFiles := lo.Filter(rrs, func(f stor.FileRecord, i int) bool {
		return f.FType != stor.FTYPE_FILE && f.FType != stor.FTYPE_DIR
	})

	// TODO: unknown types

	slices.SortFunc(rDirs, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	slices.SortFunc(rFiles, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	slices.SortFunc(oFiles, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	for _, rr := range rDirs {
		files = append(files, FileRecord{Data: rr})
	}

	for _, rr := range rFiles {
		files = append(files, FileRecord{Data: rr})
	}

	for _, rr := range oFiles {
		files = append(files, FileRecord{Data: rr})
	}

	fl.files = files

	return nil
}

func (fl *FilesList) onClicked(record stor.FileRecord) {
	fl.vp.PushPath(int(record.ID))
}

// FileRecord -----------------------------------------------------------------

type FileRecord struct {
	Data stor.FileRecord

	click widget.Clickable
}

func (kv *FileRecord) Layout(th *material.Theme, gtx layout.Context, onClicked func(stor.FileRecord)) layout.Dimensions {

	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	if kv.click.Clicked(gtx) && onClicked != nil {
		if kv.Data.FType == stor.FTYPE_DIR {
			onClicked(kv.Data)
		}
	}

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	icon := icons.FileAttachment
	if kv.Data.FType == stor.FTYPE_DIR {
		icon = icons.FileFolder
	}

	// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
	return material.Clickable(gtx, &kv.click, func(gtx layout.Context) layout.Dimensions {

		return mainLayout.Layout(gtx,
			// icon
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				size := 16
				gtx.Constraints = layout.Exact(image.Pt(size, size))
				ic, _ := widget.NewIcon(icon)
				return ic.Layout(gtx, th.ContrastBg)
			}),
			layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
			// name
			layout.Flexed(2, func(gtx layout.Context) layout.Dimensions {
				// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
				return material.Body1(th, kv.Data.Name).Layout(gtx)
			}),
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
			// size
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				return material.Body2(th, fmt.Sprintf("%d", kv.Data.Size)).Layout(gtx)
			}),

			// created
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				return material.Body1(th, kv.Data.ModTime.Format(time.DateTime)).Layout(gtx)
			}),
		)

	})
}
