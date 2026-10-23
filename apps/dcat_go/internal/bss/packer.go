package bss

import (
	"bytes"
)

// Pack - упаковать структуру в бинарный формат
func Pack(volume Volume) (*bytes.Buffer, error) {
	buf := new(bytes.Buffer)

	// file header ----------------------------------------
	err := makeFileHeader(buf)
	if err != nil {
		return buf, err
	}

	// volume description ---------------------------------
	err = makeVolumeHeader(buf, volume.Description, len(volume.Records))
	if err != nil {
		return buf, err
	}

	// file records ---------------------------------------
	for _, fr := range volume.Records {
		err = writeFileRecord(buf, fr)
		if err != nil {
			return buf, err
		}
	}

	return buf, nil
}

// Unpack - распаковать бинарный формат в структуру
func Unpack(data []byte) (Volume, error) {

	buf := bytes.NewReader(data)

	// file header ----------------------------------------
	_, err := readFileHeader(buf)
	if err != nil {
		return Volume{}, err
	}

	// voleme description + records length ----------------
	vd, records, err := readVolumeHeader(buf)
	if err != nil {
		return Volume{}, err
	}

	// file records ---------------------------------------
	allRecords := []FileRecord{}
	for range records {
		fr, err := readFileRecord(buf)
		if err != nil {
			return Volume{}, err
		}
		allRecords = append(allRecords, fr)

	}

	return Volume{
		Description: vd,
		Records:     allRecords,
	}, nil
}
