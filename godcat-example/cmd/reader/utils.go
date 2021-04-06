package main

import (
	"compress/gzip"
	"encoding/binary"
)

func ushort2(src *gzip.Reader) (uint16, error) {
	r := make([]byte, 2)
	_, err := src.Read(r)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint16(r), nil
}

type StreamReader struct {
	b []byte
	n int
}

func NewStreamReader(b []byte) *StreamReader {
	sr := &StreamReader{
		b: b,
		n: 0,
	}
	return sr
}

func (sr *StreamReader) ReadUShort2() uint16 {
	data := binary.LittleEndian.Uint16(sr.b[sr.n : sr.n+2])
	sr.n += 2
	return data
}

func (sr *StreamReader) ReadUInt4() uint32 {
	data := binary.LittleEndian.Uint32(sr.b[sr.n : sr.n+4])
	sr.n += 4
	return data
}

func (sr *StreamReader) ReadULong8() uint64 {
	data := binary.LittleEndian.Uint64(sr.b[sr.n : sr.n+8])
	sr.n += 8
	return data
}

func GetFileRecordName(r *FileRecord, h *Heap) string {
	name := h.GetString(r.NPos, r.NSize)
	return name
}
