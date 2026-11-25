package volume

import (
	"dcat/internal/app/proapp"
	"dcat/internal/ui/pro/appstate"
	"fmt"
	"path"
	"time"
)

type CloseModalCb func()

type VolumeService struct {
	app          *proapp.App
	appState     *appstate.AppState
	closeModalCb CloseModalCb
}

func NewVolumeService(app *proapp.App, appState *appstate.AppState, closeModalCb CloseModalCb) VolumeService {
	return VolumeService{
		app:          app,
		appState:     appState,
		closeModalCb: closeModalCb,
	}
}

func (evs VolumeService) CloseVolumeModal() {
	evs.closeModalCb()
}

func (evs VolumeService) Refresh() {
	evs.appState.ReadVolumes()
	evs.closeModalCb()
}

func (evs VolumeService) MakeVolume(vd proapp.VolumeDescription, ch chan interface{}) {
	ch <- ProcessStartMsg{}

	files, err := proapp.Scan(vd.ScanPath)

	if err != nil {
		fmt.Println(err)
		ch <- ProcessErrorMsg{Error: err}
		return
	}

	vd.Created = time.Now()

	// TODO: имя может быть невалидным для файловой системы
	targetFileName := fmt.Sprintf("%s.gz", vd.Name)
	targetFilePath := path.Join(evs.app.StoragePath, targetFileName)
	writeModel := proapp.Volume{
		Description: vd,
		Records:     files,
	}

	err = proapp.WriteVolumeFile(targetFilePath, writeModel)
	if err != nil {
		fmt.Println(err)
		ch <- ProcessErrorMsg{Error: err}
		return
	}

	ch <- ProcessEndMsg{}
}

type ProcessStartMsg struct{}
type ProcessEndMsg struct{}
type ProcessErrorMsg struct {
	Error error
}
