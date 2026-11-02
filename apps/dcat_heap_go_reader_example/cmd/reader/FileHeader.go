package main

import (
	"encoding/binary"
	"fmt"
)

const FileHeaderSize = 4

type FileHeader struct {
	Magic   uint16
	Version uint16
}

func NewFileHeader(bdata []byte) *FileHeader {
	f := &FileHeader{
		Magic:   binary.LittleEndian.Uint16(bdata[0:2]),
		Version: binary.LittleEndian.Uint16(bdata[2:4]),
	}

	return f
}

func (f *FileHeader) String() string {
	return fmt.Sprintln("magic: ", f.Magic, ", version: ", f.Version)
}

// class FileHeader:
// 	MAGIC = 0xfafb
// 	VERSION = 1
// 	BDATA_SIZE = 4
// 	def __init__(self):
// 		self.magic = 0xfafb
// 		self.version = 1

// 	#--- bin data -------------------------------------------------------------
// 	def unpack(self, bdata: bytes):
// 		self.magic, self.version = struct.unpack("<HH", bdata)

// 	def pack(self) -> bytes:
// 		row_tuple = (self.magic, self.version)
// 		bdata = struct.pack("<HH", *row_tuple)
// 		return bdata

// 	#--- bin data -------------------------------------------------------------

// 	def __str__(self):
// 		return "magic: {}, version: {}".format(self.magic, self.version)
