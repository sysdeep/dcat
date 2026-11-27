package mvsv2

import (
	"database/sql"
	"fmt"
)

func (m *MVSv2) CreateVolume(vol DBVolume) (int64, error) {
	query := `
		INSERT INTO "volumes" ("name", "scan_path", "created", "vtype", "description")
		VALUES (?, ?, ?, ?, ?)
		RETURNING "id";
	`

	// Если описание пустое, запишем в базу NULL вместо пустой строки (по желанию)
	var desc sql.NullString
	if vol.Description != "" {
		desc = sql.NullString{String: vol.Description, Valid: true}
	}

	var newID int64
	err := m.db.QueryRow(
		query,
		vol.Name,
		vol.ScanPath,
		vol.Created,
		vol.VType,
		desc,
	).Scan(&newID)

	if err != nil {
		return 0, fmt.Errorf("ошибка вставки тома: %w", err)
	}

	return newID, nil
}
