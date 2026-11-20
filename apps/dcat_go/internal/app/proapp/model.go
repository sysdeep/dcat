package proapp

import (
	"dcat/internal/bssv2"
	"time"
)

const (
	FTYPE_UNKNOWN = 0
	FTYPE_DIR     = 1
	FTYPE_FILE    = 2
)

type Volume struct {
	Description VolumeDescription
	Records     []FileRecord
}

type VolumeDescription struct {
	FilePath    string
	Created     time.Time // дата создания(unix timestamp)
	Icon        int       // icon_id
	Name        string    // название тома
	ScanPath    string    // путь сканирования
	Description string    // произвольное описание
}

type FileRecord struct {
	ID       uint64
	ParentID uint64
	Size     uint64
	FType    uint16 // тип, 1 - каталог, 2 - файл
	Name     string
	ModTime  time.Time
}

func toBSS(val Volume) bssv2.Volume {

	bRecords := []bssv2.FileRecord{}
	for _, r := range val.Records {
		bRecords = append(bRecords, bssv2.FileRecord{
			ID:     r.ID,
			Parent: r.ParentID,
			Name:   r.Name,
			Size:   r.Size,
			FType:  r.FType,
			CTime:  uint64(r.ModTime.Unix()),
		})
	}

	return bssv2.Volume{
		Description: bssv2.VolumeDescription{
			Created:     uint64(val.Description.Created.Unix()),
			Icon:        uint16(val.Description.Icon),
			Name:        val.Description.Name,
			ScanPath:    val.Description.ScanPath,
			Description: val.Description.Description,
			Records:     uint64(len(bRecords)),
		},
		Records: bRecords,
	}
}

func fromBBSVolume(val bssv2.Volume, filePath string) Volume {

	sRecords := []FileRecord{}
	for _, r := range val.Records {
		sRecords = append(sRecords, FileRecord{
			ID:       r.ID,
			ParentID: r.Parent,
			Name:     r.Name,
			Size:     r.Size,
			FType:    r.FType,
			ModTime:  time.Unix(int64(r.CTime), 0),
		})
	}

	return Volume{
		Description: fromBSSVolumeDescription(val.Description, filePath),
		Records:     sRecords,
	}
}

func fromBSSVolumeDescription(vd bssv2.VolumeDescription, filePath string) VolumeDescription {
	return VolumeDescription{
		Created:     time.Unix(int64(vd.Created), 0),
		Icon:        int(vd.Icon),
		Name:        vd.Name,
		ScanPath:    vd.ScanPath,
		Description: vd.Description,
		FilePath:    filePath,
	}
}
