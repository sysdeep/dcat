package files

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"
	"dcat/internal/ui/pro/rc"
	"fmt"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type C = layout.Context
type D = layout.Dimensions

var defaultMargin = unit.Dp(10)

type Files struct {
	th       *material.Theme
	appState *appstate.AppState

	// listState *widget.List
	listView *material.ListStyle
	filesBtn []widget.Clickable

	navBar     *NavBar
	volumeInfo *VolumeInfo
}

func NewFiles(th *material.Theme, appState *appstate.AppState) *Files {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)

	return &Files{
		th:         th,
		appState:   appState,
		listView:   &listView,
		filesBtn:   make([]widget.Clickable, 0),
		navBar:     NewNavBar(th, appState),
		volumeInfo: NewVolumeInfo(th, appState),
	}
}

func (fls *Files) Layout(gtx C) D {

	if len(fls.filesBtn) < len(fls.appState.CurrentFiles) {
		need := len(fls.appState.CurrentFiles) - len(fls.filesBtn)
		fls.filesBtn = append(fls.filesBtn, make([]widget.Clickable, need)...)
	}

	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		layout.Rigid(material.H6(fls.th, "Files frame").Layout),
		layout.Rigid(fls.navBar.Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

			currentFiles := fls.appState.CurrentFiles
			// Вызываем макет
			return fls.listView.Layout(gtx, len(currentFiles), func(gtx layout.Context, i int) layout.Dimensions {
				return layout.UniformInset(2).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

					if fls.filesBtn[i].Clicked(gtx) {
						fls.onFileClicked(currentFiles[i])
					}

					return fls.fileLayout(gtx, currentFiles[i], &fls.filesBtn[i])

				})
			})
		}),
		layout.Rigid(fls.volumeInfo.Layout),
	)

	// return material.Body1(mui.th, "Files frame").Layout(gtx)
}

func (fls *Files) fileLayout(gtx C, fr proapp.FileRecord, btn *widget.Clickable) D {
	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	// if vr.btnClick.Clicked(gtx) && onClicked != nil {
	// 	onClicked(vr.fr)
	// }

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	// icon := icons.FileAttachment
	// if fr.FType == proapp.FTYPE_DIR {
	// 	icon = icons.FileFolder
	// }

	img, ok := rc.FileTypeImagesMap[int(fr.FType)]
	if !ok {
		img = rc.FileTypeImagesMap[rc.FileTypeUnknown]
	}

	// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
	return material.Clickable(gtx, btn, func(gtx layout.Context) layout.Dimensions {

		return mainLayout.Layout(gtx,
			// // icon
			// layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			// 	size := 16
			// 	gtx.Constraints = layout.Exact(image.Pt(size, size))
			// 	ic, _ := widget.NewIcon(icon)
			// 	return ic.Layout(gtx, fls.th.ContrastBg)
			// }),

			// image
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {

				ic := widget.Image{
					Src: img,
				}
				return ic.Layout(gtx)
			}),

			// spacer
			layout.Rigid(layout.Spacer{Width: unit.Dp(4)}.Layout),
			// name
			layout.Flexed(2, func(gtx layout.Context) layout.Dimensions {
				// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
				return material.Body1(fls.th, fr.Name).Layout(gtx)
			}),
			layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),

			// size
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
				return material.Body2(fls.th, fmt.Sprintf("%d", fr.Size)).Layout(gtx)
			}),
		)

	})
}

func (fls *Files) onFileClicked(fr proapp.FileRecord) {
	if fr.FType == proapp.FTYPE_DIR {
		fls.appState.PushFolder(fr)
	}
}
