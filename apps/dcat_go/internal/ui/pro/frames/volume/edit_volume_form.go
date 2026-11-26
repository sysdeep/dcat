package volume

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/rc"
	"fmt"
	"image/color"
	"log/slog"
	"sync/atomic"

	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"gioui.org/x/explorer"
)

var editorBorderColor = color.NRGBA{R: 200, B: 200, G: 200, A: 250}
var iconBorderColor = color.NRGBA{R: 100, B: 200, G: 100, A: 250}
var volumeIcons = []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

// TODO: validation
// TODO: progress bar
// TODO: scanning

/*
каталог 		edit 		select_button
название 		edit
иконка 			combobox 	icon_preview
description
progressbar

запуск 						закрыть
*/
type EditVolumeForm struct {
	th    *material.Theme
	isNew bool

	log *slog.Logger

	scanPathEditor    widget.Editor
	openScanPathBtn   widget.Clickable
	nameEditor        widget.Editor
	descriptionEditor widget.Editor
	iconsListState    widget.List
	iconsBtns         []widget.Clickable

	// volumeDescription proapp.VolumeDescription
	iconId int

	// select folder
	ex              *explorer.Explorer
	pendingScanPath atomic.Pointer[string] // развязка от потока
}

func NewEditVolumeForm(th *material.Theme, isNew bool, ex *explorer.Explorer,
	initialVD proapp.VolumeDescription, log *slog.Logger) *EditVolumeForm {
	evf := EditVolumeForm{
		th:        th,
		log:       log,
		isNew:     isNew,
		iconsBtns: make([]widget.Clickable, len(volumeIcons)),
		ex:        ex,
	}

	evf.iconsListState.Gap = 2
	evf.iconsListState.Alignment = layout.Middle

	evf.scanPathEditor.SingleLine = true
	evf.nameEditor.SingleLine = true
	evf.descriptionEditor.SingleLine = false
	evf.descriptionEditor.Submit = false

	if !isNew {
		evf.nameEditor.SetText(initialVD.Name)
		evf.descriptionEditor.SetText(initialVD.Description)
		evf.iconId = initialVD.Icon
	}

	return &evf
}

func (ev *EditVolumeForm) Layout(gtx layout.Context) layout.Dimensions {

	// если горутина положила новый путь — обновляем Editor в основном потоке
	if p := ev.pendingScanPath.Swap(nil); p != nil {
		ev.scanPathEditor.SetText(*p)
	}

	if ev.openScanPathBtn.Clicked(gtx) {
		go func() {
			if path, err := ev.ex.ChooseFolder(); err == nil {
				// сохраняем в безопасной переменной
				ev.pendingScanPath.Store(&path)
				fmt.Println(path)
				gtx.Execute(op.InvalidateCmd{})
			}
		}()
	}

	return layout.Flex{Axis: layout.Vertical, Gap: 16}.Layout(gtx,

		// scan path
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			if !ev.isNew {
				return layout.Dimensions{}
			}

			return layout.Flex{Alignment: layout.Middle, Gap: 16}.Layout(gtx,
				// label
				layout.Flexed(2, material.Body1(ev.th, "Каталог").Layout),
				// edit
				layout.Flexed(10, func(gtx layout.Context) layout.Dimensions {
					return ev.editorLayout(gtx, &ev.scanPathEditor, "", false)
				}),
				// btn
				layout.Flexed(1, material.Button(ev.th, &ev.openScanPathBtn, "Выбрать").Layout),
			)
		}),
		// name
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			return layout.Flex{Alignment: layout.Middle, Gap: 16}.Layout(gtx,
				layout.Flexed(2, material.Body1(ev.th, "Название тома").Layout),
				layout.Flexed(10, func(gtx layout.Context) layout.Dimensions {
					return ev.editorLayout(gtx, &ev.nameEditor, "", false)
				}),
				layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
					return layout.Dimensions{}
				}),
			)
		}),
		// icon
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			return layout.Flex{Alignment: layout.Middle, Gap: 16}.Layout(gtx,
				layout.Flexed(2, material.Body1(ev.th, "Иконка").Layout),
				layout.Flexed(11, ev.iconsLayout),
			)
		}),

		// description
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			return layout.Flex{Alignment: layout.Baseline, Gap: 16}.Layout(gtx,
				layout.Flexed(2, material.Body1(ev.th, "Описание").Layout),
				layout.Flexed(10, func(gtx layout.Context) layout.Dimensions {
					return ev.editorLayout(gtx, &ev.descriptionEditor, "", true)
				}),
				layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
					return layout.Dimensions{}
				}),
			)
		}),

		// progress
		// layout.Rigid(func(gtx layout.Context) layout.Dimensions {
		// 	return material.ProgressBar(ev.th, 0.34).Layout(gtx)
		// }),
	)
}

func (ev *EditVolumeForm) editorLayout(gtx layout.Context, editor *widget.Editor, hint string, isDescription bool) layout.Dimensions {

	return widget.Border{Color: editorBorderColor, Width: unit.Dp(1), CornerRadius: unit.Dp(4)}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		return layout.UniformInset(unit.Dp(9)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

			if isDescription {
				// Задаём минимальную и максимальную высоту поля (например, 4–5 строк)
				gtx.Constraints.Min.Y = 100
				gtx.Constraints.Max.Y = 150
			}

			return material.Editor(ev.th, editor, hint).Layout(gtx)
		})
	})
}

func (ev *EditVolumeForm) iconsLayout(gtx layout.Context) layout.Dimensions {
	return material.List(ev.th, &ev.iconsListState).Layout(gtx, len(volumeIcons), func(gtx layout.Context, i int) layout.Dimensions {

		imgID := volumeIcons[i]

		if ev.iconsBtns[i].Clicked(gtx) {
			ev.iconId = imgID
		}

		img := rc.VolumeImagesMap[imgID]
		ic := widget.Image{
			Src: img,
		}

		if imgID == ev.iconId {
			return widget.Border{Color: iconBorderColor, Width: unit.Dp(1), CornerRadius: unit.Dp(4)}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
				return layout.UniformInset(unit.Dp(8)).Layout(gtx, ic.Layout)
			})
		}

		return material.Clickable(gtx, &ev.iconsBtns[i], func(gtx layout.Context) layout.Dimensions {
			return layout.UniformInset(unit.Dp(8)).Layout(gtx, ic.Layout)
		})

	})
}

func (ev *EditVolumeForm) GetModel() proapp.VolumeDescription {
	return proapp.VolumeDescription{
		Icon:        ev.iconId,
		Name:        ev.nameEditor.Text(),
		ScanPath:    ev.scanPathEditor.Text(),
		Description: ev.descriptionEditor.Text(),

		//
		// Created: ,
		// FilePath: ,
	}
}
