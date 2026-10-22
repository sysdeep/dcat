package stor

import (
	"compress/gzip"
	"dcat/internal/bss"
	"fmt"
	"io"
	"os"
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
	// Path     string
}

// type Stor struct{}

// func NewStor() *Stor {
// 	return &Stor{}
// }

func Read(filePath string) (Volume, error) {

	file, err := os.Open(filePath)
	if err != nil {
		return Volume{}, err
	}
	defer file.Close()

	// 2. Создаем gzip-ридер поверх открытого файла
	gzipReader, err := gzip.NewReader(file)
	if err != nil {
		return Volume{}, err
	}
	defer gzipReader.Close()

	// Вариант А: Если файл небольшой, читаем его целиком в память
	bb, err := io.ReadAll(gzipReader)
	if err != nil {
		return Volume{}, err
	}

	//------------------

	// bb, err := os.ReadFile(filePath)
	// if err != nil {
	// 	return Volume{}, err
	// }

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

	// NOTE: без сжатия
	// return os.WriteFile(filePath, buf.Bytes(), 0o666)

	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	// 2. Оборачиваем файл в gzip.Writer
	gw := gzip.NewWriter(file)
	defer gw.Close()

	// 3. Пишем данные (как в обычный файл)
	_, err = gw.Write(buf.Bytes())
	return err
}

func ToBSS(val Volume) bss.Volume {

	bRecords := []bss.FileRecord{}
	for _, r := range val.Records {
		bRecords = append(bRecords, bss.FileRecord{
			ID:      r.ID,
			Parent:  r.ParentID,
			Name:    r.Name,
			Size:    r.Size,
			FType:   r.FType,
			ModTime: uint64(r.ModTime.Unix()),
		})
	}

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
			FType:    r.FType,
			ModTime:  time.Unix(int64(r.ModTime), 0),
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
