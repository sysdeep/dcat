package mvs

func (m *MVS) GetSystem() (map[string]string, error) {

	result := map[string]string{}

	query := `
		SELECT 
			key, value
		FROM system
	`

	rows, err := m.db.Query(query)
	if err != nil {
		return result, err
	}
	defer rows.Close()

	for rows.Next() {
		var key string
		var value string

		err := rows.Scan(&key, &value)
		if err != nil {
			return result, err
		}

		result[key] = value

	}
	return result, nil
}
