package mvsv2

import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

// TODO
// MVSv2 - multi volume sqlite storage
type MVSv2 struct {
	FilePath string
	db       *sql.DB
}

func NewMVSv2(filePath string) (*MVSv2, error) {

	db, err := initDB(filePath)
	if err != nil {
		return nil, err
	}

	return &MVSv2{
		FilePath: filePath,
		db:       db,
	}, nil
}

func initDB(dbPath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("error db opening: %w", err)
	}

	// Рекомендуется для SQLite при работе в режиме WAL, чтобы избежать ошибок "database is locked"
	db.SetMaxOpenConns(1)

	// Ping() заставляет драйвер реально подключиться и создать файл БД, если его нет
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("error db connection: %w", err)
	}

	// Безопасно создаем таблицы и индексы (если их еще нет)
	if _, err := db.Exec(INIT_DB_SQL); err != nil {
		return nil, fmt.Errorf("error db initialization: %w", err)
	}

	return db, nil
}

const INIT_DB_SQL = `
	CREATE TABLE IF NOT EXISTS "volumes" (
        "id"        	INTEGER PRIMARY KEY AUTOINCREMENT,
        "name"      	VARCHAR(64) NOT NULL,
        "scan_path"     VARCHAR(256) NOT NULL,
        "created"   	INTEGER NOT NULL,		-- timestamp
        "updated"   	INTEGER DEFAULT 0,		-- timestamp
        "vtype"         INTEGER NOT NULL,
        "description"   TEXT
    );


	CREATE TABLE IF NOT EXISTS "files" (
        "id"            INTEGER NOT NULL,
        "parent_id"     INTEGER NOT NULL,
        "volume_id"     INTEGER NOT NULL,
        "name"          VARCHAR(64) NOT NULL,
        "type"          INTEGER NOT NULL,
        "ctime"         INTEGER NOT NULL, -- timestamp
        "size"          INTEGER NOT NULL
    );


	CREATE INDEX IF NOT EXISTS idx_files_volume_parent ON files(volume_id, parent_id);
`

// TODO
const SYSTEM_SQL = `

CREATE TABLE "system" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "key"       VARCHAR(64),
        "value"     VARCHAR(64)
    );
	`
