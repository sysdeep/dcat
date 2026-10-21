package stor

import (
	"dcat/internal/bss"
	"fmt"
	"os"
	"time"
)

type Volume struct {
	Description VolumeDescription
	Records     []FileRecord
}

type VolumeDescription struct {
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
	IsDir    bool
	Name     string
	Path     string
}

// type Stor struct{}

// func NewStor() *Stor {
// 	return &Stor{}
// }

func Read(filePath string) (Volume, error) {
	bb, err := os.ReadFile(filePath)
	if err != nil {
		return Volume{}, err
	}

	bssVolume, err := bss.Unpack(bb)
	if err != nil {
		return Volume{}, err
	}

	return ToStorVolume(bssVolume), nil
}

func Write(filePath string, vol Volume) error {
	bssVolume := ToBSS(vol)

	buf, err := bss.Pack(bssVolume)
	if err != nil {
		return err
	}

	return os.WriteFile(filePath, buf.Bytes(), 0o666)
}

func ToBSS(val Volume) bss.Volume {

	bRecords := []bss.FileRecord{}
	for _, r := range val.Records {
		bRecords = append(bRecords, bss.FileRecord{
			ID:     r.ID,
			Parent: r.ParentID,
			Name:   r.Name,
			Size:   r.Size,
			IsDir:  r.IsDir,
		})
	}

	fmt.Println("created before: ", val.Description.Created.Unix(), uint64(val.Description.Created.Unix()))
	return bss.Volume{
		Description: bss.VolumeDescription{
			Created:     uint64(val.Description.Created.Unix()),
			Icon:        uint16(val.Description.Icon),
			Name:        val.Description.Name,
			ScanPath:    val.Description.ScanPath,
			Description: val.Description.Description,
		},
		Records: bRecords,
	}
}

func ToStorVolume(val bss.Volume) Volume {

	sRecords := []FileRecord{}
	for _, r := range val.Records {
		sRecords = append(sRecords, FileRecord{
			ID:       r.ID,
			ParentID: r.Parent,
			Name:     r.Name,
			Size:     r.Size,
			IsDir:    r.IsDir,
		})
	}

	fmt.Println("created after: ", val.Description.Created)

	return Volume{
		Description: VolumeDescription{
			Created:     time.Unix(int64(val.Description.Created), 0),
			Icon:        int(val.Description.Icon),
			Name:        val.Description.Name,
			ScanPath:    val.Description.ScanPath,
			Description: val.Description.Description,
		},
		Records: sRecords,
	}
}
