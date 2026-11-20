package bssv2

import (
	"encoding/binary"
	"errors"
	"fmt"
	"io"
)

func Unpack(buf io.Reader) (Volume, error) {
	var expected_magic = uint64(MAGIC)

	// magic
	magic, err := readUInt64(buf)
	if err != nil {
		return Volume{}, err
	}

	if magic != expected_magic {
		return Volume{}, fmt.Errorf("expected magic: %#X, got: %#X", expected_magic, magic)
	}

	// format description
	err = readFormatDescription(buf)
	if err != nil {
		return Volume{}, err
	}

	// volume description
	vd, err := readVolumeDescription(buf)
	if err != nil {
		return Volume{}, err
	}

	// file records
	allRecords := []FileRecord{}
	for range vd.Records {
		fr, err := readFileRecord(buf)
		if err != nil {
			return Volume{}, err
		}
		allRecords = append(allRecords, fr)
	}

	// final_magic
	final_magic, err := readUInt64(buf)
	if err != nil {
		return Volume{}, err
	}

	if final_magic != expected_magic {
		return Volume{}, fmt.Errorf("expected final_magic: %#x, got: %#x", expected_magic, final_magic)
	}

	return Volume{
		Description: vd,
		Records:     allRecords,
	}, nil

}

func readFormatDescription(r io.Reader) error {
	var res uint64
	var err error
	for range 3 {
		err = binary.Read(r, binary.LittleEndian, &res)
		if err != nil {
			return err
		}
	}
	return nil
}

func readVolumeDescription(r io.Reader) (VolumeDescription, error) {

	var err error

	created, err := readUInt64(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	records, err := readUInt64(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	icon, err := readUInt16(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	name, err := readString(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	scanPath, err := readString(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	desc, err := readString(r)
	if err != nil {
		return VolumeDescription{}, err
	}

	return VolumeDescription{
		Name:        name,
		Records:     records,
		Description: desc,
		ScanPath:    scanPath,
		Created:     created,
		Icon:        icon,
	}, nil
}

func readFileRecord(r io.Reader) (FileRecord, error) {
	var err error

	id, err := readUInt64(r)
	if err != nil {
		return FileRecord{}, err
	}

	parent, err := readUInt64(r)
	if err != nil {
		return FileRecord{}, err
	}

	size, err := readUInt64(r)
	if err != nil {
		return FileRecord{}, err
	}

	cTime, err := readUInt64(r)
	if err != nil {
		return FileRecord{}, err
	}

	ftype, err := readUInt16(r)
	if err != nil {
		return FileRecord{}, err
	}

	name, err := readString(r)
	if err != nil {
		return FileRecord{}, err
	}

	return FileRecord{
		ID:     id,
		Parent: parent,
		Size:   size,
		Name:   name,
		FType:  ftype,
		CTime:  cTime,
	}, nil
}

func readUInt16(r io.Reader) (uint16, error) {
	var res uint16
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readUInt32(r io.Reader) (uint32, error) {
	var res uint32
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readUInt64(r io.Reader) (uint64, error) {
	var res uint64
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readString(r io.Reader) (string, error) {
	// 1. Читаем длину строки (2 байта)
	var length uint16
	err := binary.Read(r, binary.LittleEndian, &length)
	if err != nil {
		return "", err
	}

	// 2. Создаем слайс байт нужной длины
	buf := make([]byte, length)

	// 3. Вычитываем ровно length байт из потока
	_, err = io.ReadFull(r, buf)
	if err != nil {
		// Если данных в потоке меньше, чем указано в длине
		if errors.Is(err, io.EOF) {
			return "", io.ErrUnexpectedEOF
		}
		return "", err
	}

	// 4. Конвертируем байты в строку
	return string(buf), nil
}
