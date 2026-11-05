package mvs

type FilesFilter struct{}

func (m *MVS) GetFiles() ([]DBFile, error) {
	/*
			CREATE TABLE "files" (
		        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
		        "volume_id"     INTEGER NOT NULL,
		        "uuid"          VARCHAR(64),
		        "parent_id"     VARCHAR(64),
		        "name"          VARCHAR(64) NOT NULL,
		        "type"          INTEGER NOT NULL,
		        "rights"        INTEGER,
		        "sowner"        VARCHAR(64),
		        "sgroup"        VARCHAR(64),
		        "ctime"         INTEGER,
		        "atime"         INTEGER,
		        "mtime"         INTEGER,
		        "category"      INTEGER,
		        "description"   TEXT,
		        "size"          INTEGER

		    );

		C
	*/

	result := []DBFile{}

	query := `
		SELECT 
			id, volume_id, uuid, parent_id, name
		FROM files;
	`

	rows, err := m.db.Query(query)
	if err != nil {
		return result, err
	}
	defer rows.Close()

	for rows.Next() {
		var model DBFile

		// var created sql.NullTime
		// var updated sql.NullTime

		err := rows.Scan(&model.ID, &model.VolumeID, &model.UUID, &model.ParentID, &model.Name)
		if err != nil {
			return result, err
		}

		// if created.Valid {
		// 	model.Created = created.Time
		// }

		// if updated.Valid {
		// 	model.Updated = updated.Time
		// }

		result = append(result, model)

	}
	return result, nil
}

// func (m *MVS) GetVolumeFiles(volumeID string) {
// 	/*
// 			CREATE TABLE "files" (
// 		        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
// 		        "volume_id"     INTEGER NOT NULL,
// 		        "uuid"          VARCHAR(64),
// 		        "parent_id"     VARCHAR(64),
// 		        "name"          VARCHAR(64) NOT NULL,
// 		        "type"          INTEGER NOT NULL,
// 		        "rights"        INTEGER,
// 		        "sowner"        VARCHAR(64),
// 		        "sgroup"        VARCHAR(64),
// 		        "ctime"         INTEGER,
// 		        "atime"         INTEGER,
// 		        "mtime"         INTEGER,
// 		        "category"      INTEGER,
// 		        "description"   TEXT,
// 		        "size"          INTEGER

// 		    );

// 		C
// 	*/
// }

// func (m *MVS) GetChildFiles(parentID string) {
// 	/*
// 			CREATE TABLE "files" (
// 		        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
// 		        "volume_id"     INTEGER NOT NULL,
// 		        "uuid"          VARCHAR(64),
// 		        "parent_id"     VARCHAR(64),
// 		        "name"          VARCHAR(64) NOT NULL,
// 		        "type"          INTEGER NOT NULL,
// 		        "rights"        INTEGER,
// 		        "sowner"        VARCHAR(64),
// 		        "sgroup"        VARCHAR(64),
// 		        "ctime"         INTEGER,
// 		        "atime"         INTEGER,
// 		        "mtime"         INTEGER,
// 		        "category"      INTEGER,
// 		        "description"   TEXT,
// 		        "size"          INTEGER

// 		    );

// 		C
// 	*/
// }
