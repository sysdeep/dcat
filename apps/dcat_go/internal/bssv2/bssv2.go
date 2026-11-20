package bssv2

const (
	FTYPE_UNKNOWN = 0
	FTYPE_DIR     = 1
	FTYPE_FILE    = 2
)

const MAGIC = 0xde9e4cee5e764387

type Volume struct {
	Description VolumeDescription
	Records     []FileRecord
}

type VolumeDescription struct {
	Created     uint64 // дата создания(unix timestamp)
	Records     uint64 // кол-во записей в базе
	Icon        uint16 // icon_id
	Name        string // название тома
	ScanPath    string // путь сканирования
	Description string // произвольное описание
}

type FileRecord struct {
	ID     uint64
	Parent uint64
	Size   uint64
	CTime  uint64
	FType  uint16
	Name   string
}
