package fyneui

import (
	"dcat/internal/app/mvsapp"
	"dcat/internal/app/state"
	"dcat/internal/stor"
	"fmt"
	"slices"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
	"github.com/samber/lo"
)

type FilesList struct {
	list     *widget.List
	vp       *state.VolumeProvider
	viewList []stor.FileRecord
	mvsApp   *mvsapp.MvsApp
	appState *AppState
}

func NewFilesList(vp *state.VolumeProvider, mvsApp *mvsapp.MvsApp, appState *AppState) *FilesList {

	fl := FilesList{
		vp:       vp,
		mvsApp:   mvsApp,
		appState: appState,
	}

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
		r := fl.viewList[id]
		if r.FType == stor.FTYPE_DIR {
			vp.PushPath(int(r.ID))
		}
	}

	fl.list = list

	vp.ConnectHandler(fl.onUpdated)
	fl.onUpdated()

	// connect
	mvsApp.Connect(mvsapp.EvOpened, fl.onStorageOpened)

	return &fl
}

func (vl *FilesList) Widget() *fyne.Container {

	content := container.NewStack(vl.list)
	return content
}

func (fl *FilesList) onUpdated() error {
	records, _ := fl.vp.GetActualRecords()

	files := []stor.FileRecord{}

	// filter
	rDirs := lo.Filter(records, func(f stor.FileRecord, i int) bool {
		return f.FType == stor.FTYPE_DIR
	})

	rFiles := lo.Filter(records, func(f stor.FileRecord, i int) bool {
		return f.FType == stor.FTYPE_FILE
	})

	oFiles := lo.Filter(records, func(f stor.FileRecord, i int) bool {
		return f.FType != stor.FTYPE_FILE && f.FType != stor.FTYPE_DIR
	})

	// sort
	slices.SortFunc(rDirs, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	slices.SortFunc(rFiles, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	slices.SortFunc(oFiles, func(a stor.FileRecord, b stor.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	// concat
	for _, rr := range rDirs {
		files = append(files, rr)
	}

	for _, rr := range rFiles {
		files = append(files, rr)
	}

	for _, rr := range oFiles {
		files = append(files, rr)
	}

	fl.viewList = files
	fl.list.Refresh()
	fl.list.UnselectAll()

	return nil
}

func (fl *FilesList) onStorageOpened() error {
	if len(fl.appState.Volumes) > 0 {
		fmt.Println(fl.appState.Volumes[0])
	}
	return nil
}
