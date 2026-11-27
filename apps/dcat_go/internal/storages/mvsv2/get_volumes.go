package mvsv2

import "time"

func (m *MVSv2) GetVolumes() ([]DBVolume, error) {

	result := []DBVolume{}

	query := `
		SELECT 
			id, name, scan_path, created, updated, vtype, description 
		FROM volumes;
	`

	rows, err := m.db.Query(query)
	if err != nil {
		return result, err
	}
	defer rows.Close()

	for rows.Next() {
		var model DBVolume

		var created int64
		var updated int64

		err := rows.Scan(&model.ID, &model.Name, &model.ScanPath, &created, &updated, &model.VType, &model.Description)
		if err != nil {
			return result, err
		}

		model.Created = time.Unix(created, 0)
		model.Updated = time.Unix(updated, 0)

		result = append(result, model)

	}
	return result, nil
}
