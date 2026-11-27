package mvsv2

import (
	"fmt"
)

func (m *MVSv2) CreateFile(f DBFile) (int64, error) {
	query := `
		INSERT INTO "files" ("id", "parent_id", "volume_id", "name", "type", "ctime", "size")
		VALUES (?, ?, ?, ?, ?, ?, ?)
		RETURNING "id";
	`

	var newID int64
	err := m.db.QueryRow(
		query,
		f.ID,
		f.ParentID,
		f.VolumeID,
		f.Name,
		f.FType,
		f.CTime,
		f.Size,
	).Scan(&newID)

	if err != nil {
		return 0, fmt.Errorf("ошибка вставки файла %q: %w", f.Name, err)
	}

	return newID, nil
}
