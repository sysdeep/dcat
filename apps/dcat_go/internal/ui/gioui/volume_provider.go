package gioui

import (
	"dcat/internal/stor"
	"fmt"
)

type ProviderHandler = func() error

type VolumeProvider struct {
	vol       *stor.Volume
	pathItems []int // тек. родительский объект
	handlers  []ProviderHandler
}

const homeID = 1

func NewVolumeProvider(vol *stor.Volume) *VolumeProvider {

	for _, r := range vol.Records {
		fmt.Printf("ID: %d, parent: %d - %s\n", r.ID, r.ParentID, r.Name)
	}

	return &VolumeProvider{
		vol:       vol,
		pathItems: []int{homeID},
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
	return v.GetRecords(v.current())
}

func (v *VolumeProvider) PushPath(itemID int) error {
	v.pathItems = append(v.pathItems, itemID)
	err := v.emitUpdate()
	return err
}

func (v *VolumeProvider) PopPath() (int, error) {
	if v.PathIsEmpty() {
		return v.current(), fmt.Errorf("path is empty")
	}

	index := len(v.pathItems) - 1
	item := v.pathItems[index]

	v.pathItems = v.pathItems[:index]

	err := v.emitUpdate()

	return item, err
}

func (v *VolumeProvider) DropPath() error {

	v.pathItems = []int{homeID}

	err := v.emitUpdate()

	return err
}

func (v *VolumeProvider) PathIsEmpty() bool {
	return len(v.pathItems) < 2
}

func (v *VolumeProvider) Volume() *stor.Volume {
	return v.vol
}

func (v *VolumeProvider) ConnectHandler(handler ProviderHandler) {
	v.handlers = append(v.handlers, handler)
}

func (v *VolumeProvider) current() int {
	return v.pathItems[len(v.pathItems)-1]
}

func (v *VolumeProvider) emitUpdate() error {
	for _, h := range v.handlers {
		err := h()
		if err != nil {
			return err
		}
	}
	return nil
}
