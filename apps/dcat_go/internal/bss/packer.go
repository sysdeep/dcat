package bss

import (
	"bytes"
	"fmt"
)

func Pack(volume Volume) (*bytes.Buffer, error) {
	buf := new(bytes.Buffer)

	err := makeFileHeader(buf)
	if err != nil {
		return buf, err
	}

	err = makeVolumeHeader(buf, volume.Description, len(volume.Records))
	if err != nil {
		return buf, err
	}

	for _, fr := range volume.Records {
		writeFileRecord(buf, fr)
	}

	return buf, nil
}

func Unpack(data []byte) (Volume, error) {

	buf := bytes.NewReader(data)

	fh, err := readFileHeader(buf)
	if err != nil {
		return Volume{}, err
	}

	fmt.Println(fh)

	vd, records, err := readVolumeHeader(buf)
	if err != nil {
		return Volume{}, err
	}

	allRecords := []FileRecord{}
	for range records {
		fr, err := readFileRecord(buf)
		if err != nil {
			return Volume{}, err
		}
		allRecords = append(allRecords, fr)

	}

	/*
		packedBytes := []byte{0x00, 0x04, 0x00, 0x00, 0x05, 0x00}
		buf := bytes.NewReader(packedBytes)

		var data MyData
		// Распаковка напрямую в структуру
		err := binary.Read(buf, binary.LittleEndian, &data)
		if err != nil {
			fmt.Println("Ошибка распаковки:", err)
			return
		}

		fmt.Printf("Value1: %d, Value2: %d\n", data.Value1, data.Value2) // 1024 5

	*/
	return Volume{
		Description: vd,
		Records:     allRecords,
	}, nil
}
