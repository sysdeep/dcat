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
// type volumeHeader struct {
// 	Created     uint32 // дата создания(unix timestamp)
// 	Icon        uint16 // icon_id
// 	Records     uint64 // кол//во записей в базе
// 	TableLen    uint32 // длина секции табличных данных
// 	HeapLen     uint64 // длина секции кучи
// 	Name        string // название тома
// 	ScanPath    string // путь сканирования
// 	Description string // произвольное описание
// }

func makeVolumeHeader(buf *bytes.Buffer, payload VolumeDescription, fileRecordsCount int) error {

	var created uint64 = payload.Created
	binary.Write(buf, binary.LittleEndian, created)

	var icon uint16 = payload.Icon
	binary.Write(buf, binary.LittleEndian, icon)

	// NOTE: нужно чтобы понять сколько итерироваться
	var records uint64 = uint64(fileRecordsCount)
	binary.Write(buf, binary.LittleEndian, records)

	appendString(buf, payload.Name)
	appendString(buf, payload.ScanPath)
	appendString(buf, payload.Description)

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

	binary.Write(buf, binary.LittleEndian, uint64(record.ID))
	binary.Write(buf, binary.LittleEndian, uint64(record.Parent))
	binary.Write(buf, binary.LittleEndian, uint64(record.Size))
	binary.Write(buf, binary.LittleEndian, uint16(record.FType))
	binary.Write(buf, binary.LittleEndian, uint64(record.ModTime))
	appendString(buf, record.Name)

	return nil
}

func readFileRecord(r *bytes.Reader) (FileRecord, error) {

	id, _ := readUInt64(r)
	parent, _ := readUInt64(r)
	size, _ := readUInt64(r)
	ftype, _ := readUInt16(r)
	modTime, _ := readUInt64(r)
	name, _ := readString(r)

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
func appendString(buf *bytes.Buffer, data string) {
	length := uint16(len(data))
	binary.Write(buf, binary.LittleEndian, length)
	buf.Write([]byte(data))
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

// func writeUInt16(buf *bytes.Buffer, v uint16) error {
// 	var records uint32 = 0
// 	binary.Write(buf, binary.LittleEndian, records)
// }
