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
