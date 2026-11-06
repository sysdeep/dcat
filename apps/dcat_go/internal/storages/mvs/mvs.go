package mvs

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

// TODO
// MVS - multi volume sqlite storage
type MVS struct {
	FilePath string
	db       *sql.DB
}

func NewMVS(filePath string) (*MVS, error) {

	db, err := sql.Open("sqlite3", filePath)
	if err != nil {
		return nil, err
	}

	return &MVS{
		FilePath: filePath,
		db:       db,
	}, nil
}
