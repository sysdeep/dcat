package domain

import "time"

// TODO: DDD
type Volume struct {
	Created     time.Time // дата создания(unix timestamp)
	Icon        int       // icon_id
	Name        string    // название тома
	ScanPath    string    // путь сканирования
	Description string    // произвольное описание
}
