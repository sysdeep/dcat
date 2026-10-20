package bss

// TODO: по факту это bss
// const MAGIC uint8 = 0xfafb
// const VERSION = 1

type Volume struct {
	Description VolumeDescription
	Records     []FileRecord
}

type VolumeDescription struct {
	Created uint64 // дата создания(unix timestamp)
	Icon    uint16 // icon_id
	Records uint64 // кол//во записей в базе
	// TableLen    uint32 // длина секции табличных данных
	// HeapLen     uint64 // длина секции кучи
	Name        string // название тома
	ScanPath    string // путь сканирования
	Description string // произвольное описание
}

type FileRecord struct {
	ID     uint64
	Parent uint64
	Name   string
	Size   uint64
}
