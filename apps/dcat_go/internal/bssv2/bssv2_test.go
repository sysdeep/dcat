package bssv2

import (
	"bytes"
	"testing"
)

func TestFull(t *testing.T) {

	payload := Volume{
		Description: VolumeDescription{
			Name:        "Volume",
			Records:     2, // NOTE: use real
			Created:     12345,
			Icon:        3,
			ScanPath:    "Path",
			Description: "description",
		},
		Records: []FileRecord{
			{
				ID:     1,
				Parent: 2,
				Size:   12,
				CTime:  23455,
				FType:  4,
				Name:   "File 1",
			},
			{
				ID:     2,
				Parent: 33,
				Size:   124,
				CTime:  234355,
				FType:  44,
				Name:   "File 2",
			},
		},
	}

	buffer := bytes.Buffer{}

	err := Pack(&payload, &buffer)
	if err != nil {
		t.Fatalf("pack error: %v", err)
	}

	vol, err := Unpack(&buffer)
	if err != nil {
		t.Fatalf("pack error: %v", err)
	}

	if vol.Description != payload.Description {
		t.Fatalf("VolumeDescription error - expected: %v, got: %v", payload.Description, vol.Description)
	}

	for i := range payload.Records {
		if vol.Records[i] != payload.Records[i] {
			t.Fatalf("VolumeRecord error - expected: %v, got: %v", payload.Records[i], vol.Records[i])
		}
	}

}

func TestRecordsLenCheck(t *testing.T) {

	payload_err := Volume{
		Description: VolumeDescription{
			Records: 0, // NOTE: special corrupted
		},
		Records: []FileRecord{
			{
				ID: 1,
			},
			{
				ID: 2,
			},
		},
	}

	buffer := bytes.Buffer{}

	err := Pack(&payload_err, &buffer)
	if err == nil {
		t.Fatal("expected error, got nill")
	}

	// TODO: надо проверить что ошибка именно та которая должна быть

}
