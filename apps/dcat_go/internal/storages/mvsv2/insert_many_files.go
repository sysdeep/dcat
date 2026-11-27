package mvsv2

import (
	"fmt"
)

func (m *MVSv2) InsertManyMaker(files <-chan DBFile) error {

	// Открываем транзакцию
	tx, err := m.db.Begin()
	if err != nil {
		return fmt.Errorf("ошибка старта транзакции: %w", err)
	}
	// Гарантируем откат, если возникнет ошибка до Commit()
	defer tx.Rollback()

	// Компилируем SQL-запрос один раз для всей пачки
	stmt, err := tx.Prepare(`
		INSERT INTO "files" ("id", "parent_id", "volume_id", "name", "type", "ctime", "size")
		VALUES (?, ?, ?, ?, ?, ?, ?);
	`)
	if err != nil {
		return fmt.Errorf("ошибка подготовки запроса: %w", err)
	}
	defer stmt.Close()

	var batchError error
	for f := range files {

		if _, err := stmt.Exec(
			f.ID,
			f.ParentID,
			f.VolumeID,
			f.Name,
			f.FType,
			f.CTime,
			f.Size,
		); err != nil {
			batchError = err
			break
		}
	}

	if batchError != nil {
		return fmt.Errorf("batchError: %w", err)
	}

	// Фиксируем все изменения разом
	if err := tx.Commit(); err != nil {
		return fmt.Errorf("ошибка коммита транзакции: %w", err)
	}

	return nil
}

// type ManyMaker struct{}

// func (mm *ManyMaker) Insert(f DBFile) error {

// }
