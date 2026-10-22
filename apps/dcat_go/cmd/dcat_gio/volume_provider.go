package main

import (
	"dcat/internal/stor"
	"fmt"
)

type ProviderHandler = func() error

type VolumeProvider struct {
	vol      stor.Volume
	current  int // тек. родительский объект
	handlers []ProviderHandler
}

func NewVolumeProvider(vol stor.Volume) *VolumeProvider {

	for _, r := range vol.Records {
		fmt.Printf("ID: %d, parent: %d - %s\n", r.ID, r.ParentID, r.Name)
	}

	return &VolumeProvider{
		vol:     vol,
		current: 1,
	}
}

func (v *VolumeProvider) GetRecords(parentID int) ([]stor.FileRecord, error) {
	res := []stor.FileRecord{}
	for _, r := range v.vol.Records {
		if r.ParentID == uint64(parentID) {
			res = append(res, r)
		}
	}
	return res, nil
}

func (v *VolumeProvider) GetActualRecords() ([]stor.FileRecord, error) {
	return v.GetRecords(v.current)
}

func (v *VolumeProvider) SetCurrent(parentID int) error {
	v.current = parentID
	for _, h := range v.handlers {
		err := h()
		if err != nil {
			return err
		}
	}

	return nil
}

func (v *VolumeProvider) ConnectHandler(handler ProviderHandler) {
	v.handlers = append(v.handlers, handler)
}
