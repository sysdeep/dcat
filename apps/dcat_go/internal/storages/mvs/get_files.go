package mvs

import "strings"

type FilesFilter struct {
	WhereVolumeID string
	WhereParentID string
}

func (m *MVS) GetFiles(filter FilesFilter) ([]DBFile, error) {
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
			id, volume_id, uuid, parent_id, name, type
		FROM files
	`

	where_query := ""
	where_terms := []string{}
	where_args := []any{}
	if len(filter.WhereVolumeID) > 0 {
		where_terms = append(where_terms, "volume_id = ?")
		where_args = append(where_args, filter.WhereVolumeID)
	}

	if len(filter.WhereParentID) > 0 {
		where_terms = append(where_terms, "parent_id = ?")
		where_args = append(where_args, filter.WhereParentID)
	}

	if len(where_terms) > 0 {
		where_query += "\nWHERE " + strings.Join(where_terms, " AND ")

	}

	query += where_query

	rows, err := m.db.Query(query, where_args...)
	if err != nil {
		return result, err
	}
	defer rows.Close()

	for rows.Next() {
		var model DBFile

		// var created sql.NullTime
		// var updated sql.NullTime

		err := rows.Scan(&model.ID, &model.VolumeID, &model.UUID, &model.ParentID, &model.Name, &model.FType)
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
