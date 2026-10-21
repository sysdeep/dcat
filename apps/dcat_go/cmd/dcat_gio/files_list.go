package main

import (
	"fmt"
	"image"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"golang.org/x/exp/shiny/materialdesign/icons"
)

type FilesList struct {
	files []*FileRecord
	vp    *VolumeProvider
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
		files = append(files, &FileRecord{Name: rr.Name, Size: int(rr.Size), IsDir: rr.IsDir})
	}

	return &FilesList{
		files: files,
		vp:    vp,
	}
}

func (fl *FilesList) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {

	list := layout.List{
		Axis: layout.Vertical,
	}

	return list.Layout(gtx, len(fl.files), func(gtx layout.Context, i int) layout.Dimensions {
		// return material.Label(th, unit.Sp(14.0), "123").Layout(gtx)
		return fl.files[i].Layout(th, gtx)
	})

	// return layout.Flex{}.Layout(gtx,
	// 	// We use weight 1 for both text and count to make them the same size.
	// 	layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
	// 		// We center align the text to the area available.
	// 		return layout.Center.Layout(gtx,
	// 			// Body1 is the default text size for reading.
	// 			material.Body1(th, "Files List").Layout)
	// 	}),
	// 	// We use an empty widget to add spacing between the text
	// 	// and the button.
	// 	layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
	// 	layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
	// 		// display the button.
	// 		// return material.Button(th, &counter.increase, "Count").Layout(gtx)
	// 		return material.Label(th, unit.Sp(100.0), "TExt").Layout(gtx)
	// 	}),
	// )
}

type FileRecord struct {
	Name  string
	IsDir bool
	Size  int
}

func (kv *FileRecord) Layout(th *material.Theme, gtx layout.Context) layout.Dimensions {
	mainLayout := layout.Flex{
		Alignment: layout.Middle,
	}

	icon := icons.FileCloudDone
	if kv.IsDir {
		icon = icons.FileFolder
	}

	return mainLayout.Layout(gtx,
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			size := 16
			gtx.Constraints = layout.Exact(image.Pt(size, size))
			ic, _ := widget.NewIcon(icon)
			return ic.Layout(gtx, th.ContrastBg)
		}),
		layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			// return material.Label(th, unit.Sp(14.0), kv.Name).Layout(gtx)
			return material.Body1(th, kv.Name).Layout(gtx)
		}),
		layout.Rigid(layout.Spacer{Height: defaultMargin}.Layout),
		layout.Flexed(1, func(gtx layout.Context) layout.Dimensions {
			return material.Body2(th, fmt.Sprintf("%d", kv.Size)).Layout(gtx)
		}),
	)
}
