package bss

import (
	"bytes"
	"encoding/binary"
	"errors"
	"io"
)

// file header ----------------------------------------------------------------
type fileHeader struct {
	Magic   uint16
	Version uint16
}

func makeFileHeader(buf *bytes.Buffer) error {

	h := fileHeader{Magic: 0xfafb, Version: 1}

	return binary.Write(buf, binary.LittleEndian, h)
}

func readFileHeader(buf *bytes.Reader) (fileHeader, error) {
	result := fileHeader{}
	err := binary.Read(buf, binary.LittleEndian, &result)

	return result, err
}

// volume header --------------------------------------------------------------
func makeVolumeHeader(buf *bytes.Buffer, payload VolumeDescription, fileRecordsCount int) error {

	var err error

	var created uint64 = payload.Created
	err = binary.Write(buf, binary.LittleEndian, created)
	if err != nil {
		return err
	}

	var icon uint16 = payload.Icon
	err = binary.Write(buf, binary.LittleEndian, icon)
	if err != nil {
		return err
	}

	// NOTE: нужно чтобы понять сколько итерироваться
	var records uint64 = uint64(fileRecordsCount)
	err = binary.Write(buf, binary.LittleEndian, records)
	if err != nil {
		return err
	}

	err = appendString(buf, payload.Name)
	if err != nil {
		return err
	}
	err = appendString(buf, payload.ScanPath)
	if err != nil {
		return err
	}
	err = appendString(buf, payload.Description)
	if err != nil {
		return err
	}

	return nil

	// return binary.Write(buf, binary.LittleEndian, h)
}

func readVolumeHeader(buf *bytes.Reader) (VolumeDescription, int, error) {

	created, err := readUInt64(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	icon, err := readUInt16(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	records, err := readUInt64(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	name, err := readString(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	scanPath, err := readString(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	desc, err := readString(buf)
	if err != nil {
		return VolumeDescription{}, 0, err
	}

	return VolumeDescription{
		Name:        name,
		Description: desc,
		ScanPath:    scanPath,
		Created:     created,
		Icon:        icon,
	}, int(records), nil
}

// file record ----------------------------------------------------------------
func writeFileRecord(buf *bytes.Buffer, record FileRecord) error {

	if err := binary.Write(buf, binary.LittleEndian, uint64(record.ID)); err != nil {
		return err
	}
	if err := binary.Write(buf, binary.LittleEndian, uint64(record.Parent)); err != nil {
		return err
	}
	if err := binary.Write(buf, binary.LittleEndian, uint64(record.Size)); err != nil {
		return err
	}
	if err := binary.Write(buf, binary.LittleEndian, uint16(record.FType)); err != nil {
		return err
	}
	if err := binary.Write(buf, binary.LittleEndian, uint64(record.ModTime)); err != nil {
		return err
	}
	if err := appendString(buf, record.Name); err != nil {
		return err
	}

	return nil
}

func readFileRecord(r *bytes.Reader) (FileRecord, error) {
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

	ftype, err := readUInt16(r)
	if err != nil {
		return FileRecord{}, err
	}

	modTime, err := readUInt64(r)
	if err != nil {
		return FileRecord{}, err
	}

	name, err := readString(r)
	if err != nil {
		return FileRecord{}, err
	}

	return FileRecord{
		ID:      id,
		Parent:  parent,
		Size:    size,
		Name:    name,
		FType:   ftype,
		ModTime: modTime,
	}, nil

}

// helpers --------------------------------------------------------------------
func appendString(buf *bytes.Buffer, data string) error {
	length := uint16(len(data))
	err := binary.Write(buf, binary.LittleEndian, length)
	if err != nil {
		return err
	}
	_, err = buf.Write([]byte(data))
	return err
}

func readString(r *bytes.Reader) (string, error) {
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

func readBool(r *bytes.Reader) (bool, error) {
	var res bool
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readUInt16(r *bytes.Reader) (uint16, error) {
	var res uint16
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readUInt32(r *bytes.Reader) (uint32, error) {
	var res uint32
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}

func readUInt64(r *bytes.Reader) (uint64, error) {
	var res uint64
	err := binary.Read(r, binary.LittleEndian, &res)
	return res, err
}
