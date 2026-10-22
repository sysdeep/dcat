package main

import (
	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

/*


<files_frame>
	<nav />
	<files_list />
</files_frame>


*/

type FilesFrame struct {
	fl *FilesList
	fn *FilesNav
	vp *VolumeProvider
}

func NewFilesFrame(vp *VolumeProvider) *FilesFrame {
	// files := []*FileRecord{
	// 	&FileRecord{Name: "File 1", Size: 1024},
	// 	&FileRecord{Name: "File 2", Size: 1024},
	// 	&FileRecord{Name: "File 3", Size: 1024},
	// 	&FileRecord{Name: "File 4", Size: 1024},
	// }
	return &FilesFrame{
		fl: NewFileList(vp),
		fn: NewFilesNav(),
		vp: vp,
	}
}

func (ff *FilesFrame) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	ll := layout.Flex{
		Axis: layout.Vertical,
	}

	return ll.Layout(gtx,
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			return ff.fn.Layout(th, gtx, ff.onGo)
		}),
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(20, func(gtx layout.Context) layout.Dimensions {
			return ff.fl.Layout(th, gtx)
		}),
	)
}

func (ff *FilesFrame) onGo(parentID int) {
	ff.vp.SetCurrent(parentID)
}

// ----------------------------------------------------------------------------
type FilesNav struct {
	goHome widget.Clickable
}

func NewFilesNav() *FilesNav {
	// files := []*FileRecord{
	// 	&FileRecord{Name: "File 1", Size: 1024},
	// 	&FileRecord{Name: "File 2", Size: 1024},
	// 	&FileRecord{Name: "File 3", Size: 1024},
	// 	&FileRecord{Name: "File 4", Size: 1024},
	// }
	return &FilesNav{}
}

func (fn *FilesNav) Layout(th *material.Theme, gtx layout.Context, onGo func(parentID int)) layout.Dimensions {

	// Проверяем, кликнул ли пользователь на этот элемент в текущем кадре
	if fn.goHome.Clicked(gtx) && onGo != nil {
		onGo(1)
	}

	ll := layout.Flex{
		Axis: layout.Horizontal,
	}

	return ll.Layout(gtx,
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {

			// list := layout.List{
			// 	Axis: layout.Horizontal,
			// }

			// return list.Layout(gtx, 2, func(gtx layout.Context, i int) layout.Dimensions {
			// 	return material.Button(th, &fn.goHome, "Home").Layout(gtx)
			// })

			return material.Button(th, &fn.goHome, "Home").Layout(gtx)
		}),
		// layout.Rigid(layout.Spacer{Height: defaultMargin, Width: 100}.Layout),
		// layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
		// 	return ff.fl.Layout(th, gtx)
		// }),
	)
}
