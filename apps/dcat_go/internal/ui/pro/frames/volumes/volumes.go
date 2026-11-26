package volumes

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"
	"dcat/internal/ui/pro/rc"

	"gioui.org/layout"
	"gioui.org/op/clip"
	"gioui.org/op/paint"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type C = layout.Context
type D = layout.Dimensions

var defaultMargin = unit.Dp(10)

// TODO: подобрать иконки
var volumeIconsMap map[int][]byte = map[int][]byte{
	1:  icons.ImageISO,                // cd
	2:  icons.ImageLandscape,          // dvd
	3:  icons.ImageLeakAdd,            // bdrom
	4:  icons.ImageLeakRemove,         // crypted
	5:  icons.ImageLens,               // folder
	6:  icons.ImageLinkedCamera,       // audio_cd
	7:  icons.ImageLooks,              // hdd
	8:  icons.ImageMonochromePhotos,   // hdd_usb
	9:  icons.ImageMovieCreation,      // flash
	10: icons.ImageMusicNote,          // sd
	11: icons.ImageNature,             // floppy
	12: icons.ImageNaturePeople,       // net
	13: icons.ImagePalette,            // tape
	14: icons.ImagePanoramaHorizontal, // other
}

type Volumes struct {
	th *material.Theme

	appState *appstate.AppState

	listView *material.ListStyle

	rowsBtn []widget.Clickable
}

func NewVolumes(th *material.Theme, appState *appstate.AppState) *Volumes {
	var listState widget.List
	listState.Axis = layout.Vertical

	listView := material.List(th, &listState)
	return &Volumes{
		th:       th,
		appState: appState,

		listView: &listView,
		rowsBtn:  make([]widget.Clickable, 0),
	}
}

func (vms *Volumes) Layout(gtx C) D {

	if len(vms.rowsBtn) < len(vms.appState.Volumes) {
		need := len(vms.appState.Volumes) - len(vms.rowsBtn)
		vms.rowsBtn = append(vms.rowsBtn, make([]widget.Clickable, need)...)
	}

	return layout.UniformInset(unit.Dp(8)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

		return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
			layout.Rigid(material.H6(vms.th, "Volumes frame").Layout),
			layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

				// копируем чтобы по нему потом пройтись согласованно, иначе в промежутке состояние меняется
				localVolumes := vms.appState.Volumes

				// Вызываем макет
				return vms.listView.Layout(gtx, len(localVolumes), func(gtx layout.Context, i int) layout.Dimensions {
					return layout.UniformInset(2).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

						if vms.rowsBtn[i].Clicked(gtx) {
							vms.onVolumeClicked(vms.appState.Volumes[i])
						}

						return vms.rowLayout(gtx, vms.appState.Volumes[i], &vms.rowsBtn[i])
					})
				})
			}),
		)

	})
}

func (vms *Volumes) rowLayout(gtx C, vd proapp.VolumeDescription, btn *widget.Clickable) D {

	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	img, ok := rc.VolumeImagesMap[vd.Icon]
	if !ok {
		img = rc.VolumeImagesMap[rc.VolumeUnknown]
	}

	isSelected := vms.appState.CurrentVolume != nil && vd.FilePath == vms.appState.CurrentVolume.Description.FilePath

	return layout.Stack{}.Layout(gtx,
		layout.Expanded(func(gtx layout.Context) layout.Dimensions {
			if isSelected {
				backgroundColor := vms.th.ContrastBg
				paint.FillShape(gtx.Ops, backgroundColor, clip.Rect{Max: gtx.Constraints.Min}.Op())
			}
			return layout.Dimensions{Size: gtx.Constraints.Min}
		}),
		layout.Stacked(func(gtx layout.Context) layout.Dimensions {
			// Оборачиваем всё в material.Clickable, чтобы добавить стандартный эффект наведения и клика (ripple)
			return material.Clickable(gtx, btn, func(gtx layout.Context) layout.Dimensions {
				return layout.UniformInset(4).Layout(gtx, func(gtx layout.Context) layout.Dimensions {

					return mainLayout.Layout(gtx,

						// image
						layout.Rigid(func(gtx layout.Context) layout.Dimensions {

							ic := widget.Image{
								Src: img,
							}
							return ic.Layout(gtx)
						}),
						// spacer
						layout.Rigid(layout.Spacer{Width: unit.Dp(8)}.Layout),
						// name
						layout.Flexed(2, func(gtx layout.Context) layout.Dimensions {
							w := material.Body1(vms.th, vd.Name)
							if isSelected {
								w.Color = vms.th.ContrastFg
							}
							return w.Layout(gtx)
						}),
					)

				})
			})
		}),
	)

}

func (vms *Volumes) onVolumeClicked(vd proapp.VolumeDescription) {
	// TODO: error
	vms.appState.ReadVolume(vd)
}
