package fyneui

import (
	"dcat/internal/app/mvsapp"
	"fmt"
)

type AppState struct {
	mvsApp          *mvsapp.MvsApp
	Volumes         []mvsapp.AppVolume
	CurrentVolumeID string
	Files           *ReactiveValue[[]mvsapp.AppFile]
}

func newAppState(mvsApp *mvsapp.MvsApp) *AppState {
	as := &AppState{
		mvsApp:  mvsApp,
		Volumes: []mvsapp.AppVolume{},
		Files:   NewReactiveValue[[]mvsapp.AppFile]([]mvsapp.AppFile{}),
	}

	mvsApp.Connect(mvsapp.EvOpened, as.onStorageOpened)

	return as
}

func (as *AppState) onStorageOpened() error {
	volumes, err := as.mvsApp.GetVolumes()
	if err != nil {
		return err
	}

	as.CurrentVolumeID = ""
	as.Volumes = volumes
	as.Files.Set([]mvsapp.AppFile{})

	return nil
}

func (as *AppState) OpenVolume(volumeID string) error {
	fmt.Println("do open volume")
	as.CurrentVolumeID = volumeID
	var parentID string = "0" // NOTE: storage arch
	files, err := as.mvsApp.GetVolumeFiles(volumeID, parentID)
	if err != nil {
		return err
	}

	as.Files.Set(files)

	return nil
}

func (as *AppState) OpenFolder(volumeID string, folderID string) error {
	fmt.Println("do open volume folder")

	as.CurrentVolumeID = volumeID
	files, err := as.mvsApp.GetVolumeFiles(volumeID, folderID)
	if err != nil {
		return err
	}

	as.Files.Set(files)

	return nil
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
