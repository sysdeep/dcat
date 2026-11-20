package appstate

import (
	"dcat/internal/app/proapp"
	"fmt"
)

type AppState struct {
	app *proapp.App

	// state
	Volumes       []proapp.VolumeDescription
	CurrentVolume *proapp.Volume
}

func NewAppState(app *proapp.App) *AppState {
	return &AppState{
		app:     app,
		Volumes: make([]proapp.VolumeDescription, 0),
	}
}

func (as *AppState) ReadVolumes() error {
	vls, err := as.app.ReadVolumes()
	if err != nil {
		return err
	}

	as.Volumes = vls
	return nil
}

func (as *AppState) ReadVolume(vd proapp.VolumeDescription) error {
	fmt.Println("read voleme: " + vd.FilePath)
	vol, err := as.app.ReadVolume(vd.FilePath)
	if err != nil {
		return err
	}

	as.CurrentVolume = &vol
	return nil
}
