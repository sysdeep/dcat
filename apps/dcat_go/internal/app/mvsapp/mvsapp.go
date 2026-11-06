package mvsapp

import (
	"dcat/internal/storages/mvs"
	"fmt"
)

type AppEvent int
type AppEventHandler func() error

const (
	EvOpened AppEvent = iota
)

type MvsApp struct {
	storage     *mvs.MVS
	handlersMap map[AppEvent][]AppEventHandler
}

func NewMvsApp() *MvsApp {
	return &MvsApp{
		handlersMap: map[AppEvent][]AppEventHandler{},
	}
}

func (m *MvsApp) Open(dbPath string) error {
	st, err := mvs.NewMVS(dbPath)

	if err != nil {
		return err
	}
	m.storage = st

	return m.emit(EvOpened)
}

func (m *MvsApp) GetVolumes() ([]AppVolume, error) {

	result := []AppVolume{}

	dbVols, err := m.storage.GetVolumes()
	if err != nil {
		return result, err
	}

	for _, dbVol := range dbVols {
		result = append(result, fromDBVolume(dbVol))
	}

	return result, nil
}

func (m *MvsApp) GetVolumeFiles(volumeID string, parentID string) ([]AppFile, error) {

	result := []AppFile{}

	filterParams := mvs.FilesFilter{
		WhereVolumeID: volumeID,
		WhereParentID: parentID,
	}

	dbfiles, err := m.storage.GetFiles(filterParams)
	if err != nil {
		return result, err
	}

	for _, dbFile := range dbfiles {
		result = append(result, fromDBFile(dbFile))
	}

	return result, nil
}

func (m *MvsApp) GetSystemInfo() (SystemInfo, error) {
	if m.storage == nil {
		return SystemInfo{}, fmt.Errorf("Storage is not opened")
	}

	sysInfo, err := m.storage.GetSystem()
	if err != nil {
		return SystemInfo{}, err
	}

	return SystemInfo{
		DBPath:      m.storage.FilePath,
		Version:     sysInfo["version"],
		Created:     sysInfo["created"],
		Updated:     sysInfo["updated"],
		Description: sysInfo["description"],
	}, nil

}

// events ---------------------------------------------------------------------
func (m *MvsApp) Connect(ev AppEvent, h AppEventHandler) {
	_, ok := m.handlersMap[ev]
	if !ok {
		m.handlersMap[ev] = []AppEventHandler{}
	}

	m.handlersMap[ev] = append(m.handlersMap[ev], h)
}

func (m *MvsApp) emit(ev AppEvent) error {
	hhs, ok := m.handlersMap[ev]
	if ok {
		for _, h := range hhs {
			err := h()
			if err != nil {
				return err
			}
		}
	}
	return nil
}
