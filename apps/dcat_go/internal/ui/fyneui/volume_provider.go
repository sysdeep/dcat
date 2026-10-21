package fyneui

import (
	"dcat/internal/stor"
	"fmt"
)

type VolumeProvider struct {
	vol stor.Volume
}

func NewVolumeProvider(vol stor.Volume) *VolumeProvider {

	for _, r := range vol.Records {
		fmt.Printf("ID: %d, parent: %d - %s\n", r.ID, r.ParentID, r.Name)
	}

	return &VolumeProvider{
		vol: vol,
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
