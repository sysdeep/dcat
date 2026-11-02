package bss

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
	Created     uint64 // дата создания(unix timestamp)
	Icon        uint16 // icon_id
	Records     uint64 // кол//во записей в базе
	Name        string // название тома
	ScanPath    string // путь сканирования
	Description string // произвольное описание
}

type FileRecord struct {
	ID      uint64
	Parent  uint64
	Name    string
	Size    uint64
	FType   uint16
	ModTime uint64
}
