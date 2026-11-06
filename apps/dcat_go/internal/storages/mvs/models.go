package mvs

import "time"

type DBVolume struct {
	ID          int
	UUID        string
	Name        string    // название тома
	ScanPath    string    // путь сканирования
	Created     time.Time // дата создания
	Updated     time.Time // дата обновления
	VType       string    //
	Description string    // произвольное описание
}

const FILE_TYPE_FOLDER = 0
const FILE_TYPE_FILE = 1

type DBFile struct {
	ID          int
	VolumeID    string // NOTE: в реальности там uuid
	UUID        string
	ParentID    string
	Name        string
	FType       int
	Rights      int
	SOwner      string
	SGroup      string
	CTime       int
	ATime       int
	MTime       int
	Category    int
	Description string
	Size        int
}
