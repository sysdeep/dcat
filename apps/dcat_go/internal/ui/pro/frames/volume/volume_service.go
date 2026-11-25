package volume

import (
	"dcat/internal/app/proapp"
	"fmt"
	"path"
	"time"
)

type CloseModalCb func()

type VolumeService struct {
	app          *proapp.App
	closeModalCb CloseModalCb
}

func NewVolumeService(app *proapp.App, closeModalCb CloseModalCb) VolumeService {
	return VolumeService{
		app:          app,
		closeModalCb: closeModalCb,
	}
}

func (evs VolumeService) CloseVolumeModal() {
	evs.closeModalCb()
}

func (evs VolumeService) MakeVolume(vd proapp.VolumeDescription) {
	files, err := proapp.Scan(vd.ScanPath)
	if err != nil {
		fmt.Println(err)
	} else {

		vd.Created = time.Now()
		// desc.FilePath = path.Join() // TODO
		targetFileName := fmt.Sprintf("%s.gz", vd.Name)
		targetFilePath := path.Join(evs.app.StoragePath, targetFileName)
		writeModel := proapp.Volume{
			Description: vd,
			Records:     files,
		}

		err = proapp.WriteVolumeFile(targetFilePath, writeModel)
		if err != nil {
			fmt.Println(err)
		}
	}
}
