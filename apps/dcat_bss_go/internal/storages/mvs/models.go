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
