package fyneui

import (
	"dcat/internal/app/mvsapp"
	"fmt"
	"slices"
	"strings"
)

type AppStateEvent int

const (
	AppStateStackChanged AppStateEvent = iota
	AppStateVolumesChanged
)

type AppStateEventHandler func() error

type AppState struct {
	mvsApp        *mvsapp.MvsApp
	Volumes       []mvsapp.AppVolume
	CurrentVolume mvsapp.AppVolume
	FoldersStack  []mvsapp.AppFile
	Files         *ReactiveValue[[]mvsapp.AppFile]
	handlers      map[AppStateEvent][]AppStateEventHandler
}

func newAppState(mvsApp *mvsapp.MvsApp) *AppState {
	as := &AppState{
		mvsApp:       mvsApp,
		Volumes:      []mvsapp.AppVolume{},
		FoldersStack: []mvsapp.AppFile{},
		Files:        NewReactiveValue[[]mvsapp.AppFile]([]mvsapp.AppFile{}),
		handlers:     map[AppStateEvent][]AppStateEventHandler{},
	}

	mvsApp.Connect(mvsapp.EvOpened, as.onStorageOpened)

	return as
}

func (as *AppState) onStorageOpened() error {
	volumes, err := as.mvsApp.GetVolumes()
	if err != nil {
		return err
	}

	as.CurrentVolume = mvsapp.AppVolume{}
	as.setVolumes(volumes)
	as.Files.Set([]mvsapp.AppFile{})

	return nil
}

func (as *AppState) OpenVolume(volume mvsapp.AppVolume) error {
	fmt.Println("do open volume")
	as.CurrentVolume = volume
	as.clearFolderStack()
	var parentID string = "0" // NOTE: storage arch
	files, err := as.mvsApp.GetVolumeFiles(as.CurrentVolume.UUID, parentID)
	if err != nil {
		return err
	}

	as.Files.Set(files)

	return nil
}

func (as *AppState) OpenFolder(folder mvsapp.AppFile) error {
	fmt.Println("do open volume folder")
	as.pushFolderStack(folder)
	files, err := as.mvsApp.GetVolumeFiles(as.CurrentVolume.UUID, as.FoldersStack[len(as.FoldersStack)-1].UUID)
	if err != nil {
		return err
	}

	as.Files.Set(as.formatFiles(files))

	return nil
}

func (as *AppState) GoBack() error {
	fmt.Println("do back")
	if len(as.FoldersStack) > 0 {
		as.popFolderStack()

		parentID := "0"
		if len(as.FoldersStack) > 0 {
			parentID = as.FoldersStack[len(as.FoldersStack)-1].UUID
		}
		files, err := as.mvsApp.GetVolumeFiles(as.CurrentVolume.UUID, parentID)
		if err != nil {
			return err
		}

		as.Files.Set(as.formatFiles(files))

	}
	return nil
}

func (as *AppState) GoInStack(i int) error {
	fmt.Println("do in stack: ", i)
	as.reduceFolderStack(i)

	parentID := "0"
	if len(as.FoldersStack) > 0 {
		parentID = as.FoldersStack[len(as.FoldersStack)-1].UUID
	}
	files, err := as.mvsApp.GetVolumeFiles(as.CurrentVolume.UUID, parentID)
	if err != nil {
		return err
	}

	as.Files.Set(as.formatFiles(files))

	return nil
}

// TODO: дублируется с OpenVolume
func (as *AppState) GoHome() error {
	fmt.Println("do home")
	as.clearFolderStack()
	var parentID string = "0" // NOTE: storage arch
	files, err := as.mvsApp.GetVolumeFiles(as.CurrentVolume.UUID, parentID)
	if err != nil {
		return err
	}

	as.Files.Set(files)
	return nil
}

func (as *AppState) formatFiles(files []mvsapp.AppFile) []mvsapp.AppFile {
	resDirs := []mvsapp.AppFile{}
	resFiles := []mvsapp.AppFile{}
	resOther := []mvsapp.AppFile{}

	for _, f := range files {
		if f.IsFolder() {
			resDirs = append(resDirs, f)
			continue
		}
		if f.IsFile() {
			resFiles = append(resFiles, f)
			continue
		}

		resOther = append(resOther, f)
	}

	cmpFunc := func(a mvsapp.AppFile, b mvsapp.AppFile) int {
		return strings.Compare(a.Name, b.Name)
	}

	slices.SortFunc(resDirs, cmpFunc)
	slices.SortFunc(resFiles, cmpFunc)
	slices.SortFunc(resOther, cmpFunc)

	return slices.Concat(resDirs, resFiles, resOther)
}

func (as *AppState) pushFolderStack(v mvsapp.AppFile) {
	as.FoldersStack = append(as.FoldersStack, v)
	as.emit(AppStateStackChanged)
}

func (as *AppState) popFolderStack() {
	as.FoldersStack = as.FoldersStack[0 : len(as.FoldersStack)-1]
	as.emit(AppStateStackChanged)
}

func (as *AppState) clearFolderStack() {
	as.FoldersStack = []mvsapp.AppFile{}
	as.emit(AppStateStackChanged)
}

func (as *AppState) reduceFolderStack(index int) {
	as.FoldersStack = as.FoldersStack[0:index]
	as.emit(AppStateStackChanged)
}

func (as *AppState) setVolumes(vs []mvsapp.AppVolume) {
	as.Volumes = vs
	as.emit(AppStateVolumesChanged)
}

// events ---------------------------------------------------------------------
func (as *AppState) Connect(e AppStateEvent, h AppStateEventHandler) {
	_, ok := as.handlers[e]
	if !ok {
		as.handlers[e] = []AppStateEventHandler{}
	}
	as.handlers[e] = append(as.handlers[e], h)
}

func (as *AppState) emit(e AppStateEvent) {
	hhs, ok := as.handlers[e]
	if ok {
		for _, h := range hhs {
			// TODO: err
			h()
		}
	}
}

// reactive value example -----------------------------------------------------

type ReactiveValue[T any] struct {
	value    T
	handlers []func()
}

func NewReactiveValue[T any](initValue T) *ReactiveValue[T] {
	return &ReactiveValue[T]{
		value:    initValue,
		handlers: []func(){},
	}
}

func (r *ReactiveValue[T]) Connect(h func()) {
	r.handlers = append(r.handlers, h)
}

func (r *ReactiveValue[T]) Set(v T) {
	r.value = v
	for _, h := range r.handlers {
		h()
	}
}

func (r *ReactiveValue[T]) Get() T {
	return r.value
}
