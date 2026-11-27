package mvsv2

import "time"

type DBVolume struct {
	ID          int
	Name        string    // название тома
	ScanPath    string    // путь сканирования
	Created     time.Time // дата создания
	Updated     time.Time // дата обновления
	VType       int       //
	Description string    // произвольное описание
}

const FILE_TYPE_FOLDER = 0
const FILE_TYPE_FILE = 1

type DBFile struct {
	ID       int64
	ParentID int64
	VolumeID int64
	Name     string
	FType    int
	CTime    time.Time
	Size     int64
}
