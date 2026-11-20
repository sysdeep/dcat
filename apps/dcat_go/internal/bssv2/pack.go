package bssv2

import (
	"encoding/binary"
	"fmt"
	"io"
)

func Pack(vol *Volume, buf io.Writer) error {

	if vol.Description.Records != uint64(len(vol.Records)) {
		return fmt.Errorf("count in description and real records len are mismatched: %d <> %d", vol.Description.Records, len(vol.Records))
	}

	var err error
	var magic uint64 = MAGIC

	// magic
	err = writeMagic(magic, buf)
	if err != nil {
		return err
	}

	// format description
	err = writeFormatDescription(buf)
	if err != nil {
		return err
	}

	// volume description
	err = writeVolumeDescription(vol.Description, buf)
	if err != nil {
		return err
	}

	// records
	for _, fr := range vol.Records {
		if err = writeFileRecord(fr, buf); err != nil {
			return err
		}
	}

	// final magic
	err = writeMagic(magic, buf)
	if err != nil {
		return err
	}

	return nil
}

func writeMagic(v uint64, buf io.Writer) error {
	return binary.Write(buf, binary.LittleEndian, v)
}

func writeFormatDescription(buf io.Writer) error {
	var pass uint64
	var err error
	for range 3 {

		err = binary.Write(buf, binary.LittleEndian, pass)
		if err != nil {
			return err
		}
	}
	return nil
}

func writeVolumeDescription(vd VolumeDescription, w io.Writer) error {

	var err error

	// created
	var created uint64 = vd.Created
	if err = binary.Write(w, binary.LittleEndian, created); err != nil {
		return err
	}

	// records
	var records uint64 = vd.Records
	if err = binary.Write(w, binary.LittleEndian, records); err != nil {
		return err
	}

	// icon
	var icon uint16 = vd.Icon
	if err = binary.Write(w, binary.LittleEndian, icon); err != nil {
		return err
	}

	if err = writeString(w, vd.Name); err != nil {
		return err
	}

	if err = writeString(w, vd.ScanPath); err != nil {
		return err
	}

	if err = writeString(w, vd.Description); err != nil {
		return err
	}

	return nil

}

func writeFileRecord(record FileRecord, w io.Writer) error {
	if err := binary.Write(w, binary.LittleEndian, uint64(record.ID)); err != nil {
		return err
	}
	if err := binary.Write(w, binary.LittleEndian, uint64(record.Parent)); err != nil {
		return err
	}
	if err := binary.Write(w, binary.LittleEndian, uint64(record.Size)); err != nil {
		return err
	}
	if err := binary.Write(w, binary.LittleEndian, uint64(record.CTime)); err != nil {
		return err
	}
	if err := binary.Write(w, binary.LittleEndian, uint16(record.FType)); err != nil {
		return err
	}
	if err := writeString(w, record.Name); err != nil {
		return err
	}

	return nil
}

func writeString(w io.Writer, data string) error {
	length := uint16(len(data))
	if err := binary.Write(w, binary.LittleEndian, length); err != nil {
		return err
	}
	_, err := w.Write([]byte(data))
	return err
}
