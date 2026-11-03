package mvs

import (
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

// TODO
// MVS - multi volume sqlite storage
type MVS struct {
	filePath string
	db       *sql.DB
}

func NewMVS(filePath string) (*MVS, error) {

	db, err := sql.Open("sqlite3", filePath)
	if err != nil {
		return nil, err
	}

	return &MVS{
		filePath: filePath,
		db:       db,
	}, nil
}

func (m *MVS) GetVolumes() ([]DBVolume, error) {
	/*
			CREATE TABLE "volumes" (
		        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
		        "uuid"      VARCHAR(64),
		        "name"      VARCHAR(64),
		        "path"      VARCHAR(256),
		        "created"   DATETIME,
		        "updated"   DATETIME,
		        "vtype"         VARCHAR(32),
		        "description"   TEXT
		    );
		`
	*/

	result := []DBVolume{}

	query := `
		SELECT 
			id, uuid, name, path, created, updated, vtype, description 
		FROM volumes;
	`

	rows, err := m.db.Query(query)
	if err != nil {
		return result, err
	}
	defer rows.Close()

	for rows.Next() {
		var model DBVolume

		var created sql.NullTime
		var updated sql.NullTime

		err := rows.Scan(&model.ID, &model.UUID, &model.Name, &model.ScanPath, &created, &updated, &model.VType, &model.Description)
		if err != nil {
			return result, err
		}

		if created.Valid {
			model.Created = created.Time
		}

		if updated.Valid {
			model.Updated = updated.Time
		}

		result = append(result, model)

	}
	return result, nil
}
