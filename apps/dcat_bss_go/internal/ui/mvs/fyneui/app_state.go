package fyneui

import "dcat/internal/app/mvsapp"

type AppState struct {
	mvsApp  *mvsapp.MvsApp
	Volumes []mvsapp.AppVolume
}

func newAppState(mvsApp *mvsapp.MvsApp) *AppState {
	as := &AppState{
		mvsApp: mvsApp,
	}

	mvsApp.Connect(mvsapp.EvOpened, as.onStorageOpened)

	return as
}

func (as *AppState) onStorageOpened() error {
	volumes, err := as.mvsApp.GetVolumes()
	if err != nil {
		return err
	}

	as.Volumes = volumes

	return nil
}
