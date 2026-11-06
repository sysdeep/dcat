package mvsapp

import (
	"dcat/internal/storages/mvs"
	"time"
)

type AppVolume struct {
	ID          int
	UUID        string
	Name        string    // название тома
	ScanPath    string    // путь сканирования
	Created     time.Time // дата создания
	Updated     time.Time // дата обновления
	VType       string    //
	Description string    // произвольное описание
}

func fromDBVolume(vol mvs.DBVolume) AppVolume {
	return AppVolume{
		ID:          vol.ID,
		UUID:        vol.UUID,
		Name:        vol.Name,
		ScanPath:    vol.ScanPath,
		Created:     vol.Created,
		Updated:     vol.Updated,
		VType:       vol.VType,
		Description: vol.Description,
	}
}

const FILE_TYPE_FOLDER = 0
const FILE_TYPE_FILE = 1

type AppFile struct {
	ID       int
	VolumeID string
	UUID     string
	ParentID string
	Name     string
	FType    int
	// Rights      int
	// SOwner      string
	// SGroup      string
	// CTime       int
	// ATime       int
	// MTime       int
	// Category    int
	// Description string
	// Size        int
}

func (f *AppFile) IsFolder() bool {
	return f.FType == FILE_TYPE_FOLDER
}

func (f *AppFile) IsFile() bool {
	return f.FType == FILE_TYPE_FILE
}

func fromDBFile(model mvs.DBFile) AppFile {
	return AppFile{
		ID:       model.ID,
		VolumeID: model.VolumeID,
		UUID:     model.UUID,
		ParentID: model.ParentID,
		Name:     model.Name,
		FType:    model.FType, // NOTE: 1by1
	}
}
