package gioui

import (
	"dcat/internal/ui/materialfactory"
	"image"

	"gioui.org/layout"
	"gioui.org/op/clip"
	"gioui.org/unit"
	"gioui.org/widget/material"
)

/*


<files_frame>
	<nav />
	<files_list />
</files_frame>


*/

const (
	goHomeID = 1
	goBackID = 2
)

type FilesFrame struct {
	fl        *FilesList
	mf        *materialfactory.MaterialFactory
	fn        *FilesNav
	openPanel *OpenPanel
	vp        *VolumeProvider
}

func NewFilesFrame(vp *VolumeProvider, mf *materialfactory.MaterialFactory) *FilesFrame {
	return &FilesFrame{
		fl:        NewFileList(vp),
		mf:        mf,
		fn:        NewFilesNav(vp, mf),
		vp:        vp,
		openPanel: NewOpenPanel(mf.Theme()),
	}
}

func (ff *FilesFrame) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	ll := layout.Flex{
		Axis: layout.Vertical,
	}

	return ll.Layout(gtx,
		layout.Rigid(ff.openPanel.Layout),
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {
			return ff.fn.Layout2(th, gtx, ff.onGo)
		}),
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(20, func(gtx layout.Context) layout.Dimensions {
			return ff.fl.Layout(th, gtx)
		}),
	)
}

func (ff *FilesFrame) onGo(actionID int) {
	switch actionID {
	case goBackID:
		ff.vp.PopPath()
	case goHomeID:
		ff.vp.DropPath()
	}

}

// ----------------------------------------------------------------------------
type FilesNav struct {
	vp        *VolumeProvider
	mf        *materialfactory.MaterialFactory
	goHomeBtn material.ButtonStyle
	goBackBtn material.ButtonStyle

	// goHomeNew  widget.Clickable
	// goHomeIcon *widget.Icon
}

func NewFilesNav(vp *VolumeProvider, mf *materialfactory.MaterialFactory) *FilesNav {

	// ic, _ := widget.NewIcon(icons.ActionHome)

	return &FilesNav{
		vp:        vp,
		mf:        mf,
		goHomeBtn: mf.Button("Home"),
		goBackBtn: mf.Button("Back"),

		// goHomeIcon: ic,
	}
}

// func (fn *FilesNav) Layout(th *material.Theme, gtx layout.Context, onGo func(parentID int)) layout.Dimensions {

// 	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
// 	if fn.goHome.Clicked(gtx) && onGo != nil {
// 		onGo(1)
// 	}

// 	ll := layout.Flex{
// 		Axis: layout.Horizontal,
// 	}

// 	return ll.Layout(gtx,
// 		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

// 			// list := layout.List{
// 			// 	Axis: layout.Horizontal,
// 			// }

// 			// return list.Layout(gtx, 2, func(gtx layout.Context, i int) layout.Dimensions {
// 			// 	return material.Button(th, &fn.goHome, "Home").Layout(gtx)
// 			// })

// 			return material.Button(th, &fn.goHome, "Home").Layout(gtx)
// 		}),
// 		// layout.Rigid(layout.Spacer{Height: defaultMargin, Width: 100}.Layout),
// 		// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
// 		// 	return ff.fl.Layout(th, gtx)
// 		// }),
// 	)
// }

func (fn *FilesNav) Layout2(th *material.Theme, gtx layout.Context, onGo func(parentID int)) layout.Dimensions {

	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	if fn.goHomeBtn.Button.Clicked(gtx) && onGo != nil {
		onGo(goHomeID)
	}

	if fn.goBackBtn.Button.Clicked(gtx) && onGo != nil && !fn.vp.PathIsEmpty() {
		onGo(goBackID)
	}

	// TODO
	// if fn.vp.PathIsEmpty() {
	// 						btn.Background = th.Palette.Bg
	// 						btn.Color = th.Palette.Fg
	// 					}

	// NOTE: в виде fullstate - надо делать метод переключения
	// if fn.vp.PathIsEmpty() {
	// 	fn.goBackBtn.Background = th.Palette.Bg
	// 	fn.goBackBtn.Color = th.Palette.Fg
	// }

	// Задаем цвет фона для панели (светло-серый)
	// backgroundColor := color.NRGBA{R: 240, G: 240, B: 240, A: 255}

	return layout.Stack{}.Layout(gtx,
		// Отрисовка подложки тулбара
		// layout.Expanded(func(gtx layout.Context) layout.Dimensions {
		// 	paint.FillShape(gtx.Ops, backgroundColor, clipRectangle(gtx.Constraints.Max))
		// 	return layout.Dimensions{Size: gtx.Constraints.Max}
		// }),
		// Размещение кнопок внутри тулбара с отступами
		layout.Stacked(func(gtx layout.Context) layout.Dimensions {
			return layout.Inset{
				Top:    unit.Dp(6),
				Bottom: unit.Dp(6),
				Left:   unit.Dp(10),
			}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {

				// Горизонтальный ряд для кнопок
				return layout.Flex{
					Axis:    layout.Horizontal,
					Spacing: layout.SpaceEnd, // Кнопки прижаты к левому краю
				}.Layout(gtx,
					layout.Rigid(fn.goHomeBtn.Layout),
					layout.Rigid(layout.Spacer{Width: unit.Dp(8)}.Layout), // Отступ между кнопками
					layout.Rigid(fn.goBackBtn.Layout),

					// NOTE: рисует круглую иконку...
					// layout.Rigid(material.IconButton(th, &fn.goHomeNew, fn.goHomeIcon, "Home").Layout),
				)
			})
		}),
	)
}

// Вспомогательная функция для создания прямоугольника
func clipRectangle(size image.Point) clip.Op {
	return clip.Rect{Max: size}.Op()
}
