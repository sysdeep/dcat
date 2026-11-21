package appstate

import (
	"dcat/internal/app/proapp"
	"fmt"
	"slices"
	"strings"
)

type AppState struct {
	app *proapp.App

	// state
	Volumes       []proapp.VolumeDescription
	CurrentVolume *proapp.Volume
	CurrentFiles  []proapp.FileRecord
}

func NewAppState(app *proapp.App) *AppState {
	return &AppState{
		app:          app,
		Volumes:      make([]proapp.VolumeDescription, 0),
		CurrentFiles: make([]proapp.FileRecord, 0),
	}
}

func (as *AppState) ReadVolumes() error {
	vls, err := as.app.ReadVolumes()
	if err != nil {
		return err
	}

	as.Volumes = vls
	as.CurrentVolume = nil
	as.CurrentFiles = make([]proapp.FileRecord, 0)

	return nil
}

func (as *AppState) ReadVolume(vd proapp.VolumeDescription) error {
	fmt.Println("read voleme: " + vd.FilePath)
	vol, err := as.app.ReadVolume(vd.FilePath)
	if err != nil {
		return err
	}

	as.CurrentVolume = &vol

	startFiles, err := as.getFiles(1) // 0 root, 1 - files in root
	if err != nil {
		return err
	}
	as.CurrentFiles = startFiles

	return nil
}

func (as *AppState) getFiles(PID uint64) ([]proapp.FileRecord, error) {
	result := make([]proapp.FileRecord, 0)
	if as.CurrentVolume == nil {
		return result, fmt.Errorf("getFiles - no current volume")
	}

	for _, fr := range as.CurrentVolume.Records {
		if fr.ParentID == PID {
			result = append(result, fr)
		}
	}

	slices.SortFunc(result, func(a, b proapp.FileRecord) int {
		return strings.Compare(a.Name, b.Name)
	})

	dirs := make([]proapp.FileRecord, 0)
	files := make([]proapp.FileRecord, 0)
	other := make([]proapp.FileRecord, 0)
	for _, fr := range result {
		if fr.FType == proapp.FTYPE_DIR {
			dirs = append(dirs, fr)
			continue
		}

		if fr.FType == proapp.FTYPE_FILE {
			files = append(files, fr)
			continue
		}

		other = append(other, fr)
	}

	result_final := make([]proapp.FileRecord, 0)
	result_final = append(result_final, dirs...)
	result_final = append(result_final, files...)
	result_final = append(result_final, other...)

	return result_final, nil
}
