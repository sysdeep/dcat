package main

import (
	"compress/gzip"
	"fmt"
	"log"
	"os"
)

const MAGIC = 64251

var dbPath = "/home/nia/Development/_Python/_DCat/Export10/app2/oxygen_16x16.hmap.gz"

func main() {
	fmt.Println("start")

	f, err := os.Open(dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	log.Println("file opened")
	fileInfo, _ := f.Stat()
	log.Println("file size: ", fileInfo.Size())

	gr, err := gzip.NewReader(f)
	if err != nil {
		log.Fatal(err)
	}
	defer gr.Close()
	log.Println("gzip opened")

	//--- file header
	fileHeaderBytes := make([]byte, FileHeaderSize)
	_, err = gr.Read(fileHeaderBytes)
	if err != nil {
		log.Fatal(err)
	}

	fh := NewFileHeader(fileHeaderBytes)
	log.Println(fh.String())

	//--- volume header
	volumeHeaderBytes := make([]byte, VolumeHeaderSize)
	_, err = gr.Read(volumeHeaderBytes)
	if err != nil {
		log.Fatal(err)
	}

	vh := NewVolumeHeader(volumeHeaderBytes)
	vh.PrintInfo()

	//--- table records
	tableBytes := make([]byte, vh.TableLength)
	var needRead uint64 = vh.TableLength
	var tableReaded uint64 = 0

	for needRead > 0 {

		readSize := 1024
		if needRead < uint64(readSize) {
			readSize = int(needRead)
		}

		buf := make([]byte, readSize)
		readed, err := gr.Read(buf)
		if err != nil {
			log.Fatal(err)
		}
		tableBytes = append(tableBytes, buf[:readed]...)
		// tableBytes[tableReaded : tableReaded+readed] = buf[:readed]...
		tableReaded += uint64(readed)
		// log.Println(tableReaded)

		needRead -= uint64(readed)

	}

	// !!! len 37640, but readed: 32712
	// tableReaded, err := gr.Read(tableBytes)
	// if err != nil {
	// 	log.Fatal(err)
	// }

	log.Println("table records len: ", vh.TableLength)
	log.Println("table records buf len: ", len(tableBytes))
	log.Println("table records readed: ", tableReaded)
	log.Println("records calculated: ", len(tableBytes)/40)

	//--- heap
	heapBytes := make([]byte, vh.HeapLength)
	heapReaded, err := gr.Read(heapBytes)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("heap readed: ", heapReaded)

	heap := NewHeap(heapBytes)

	log.Println("volume name:", heap.GetString(vh.NPos, vh.NSize)) // должно быть... b'6f787967656e5f3136783136' а есть: 10 0 9 53 0 0 0 0 1 0 57 2
	log.Println("volume path:", heap.GetString(vh.PPos, vh.PSize))
	log.Println("volume desc:", heap.GetString(vh.DPos, vh.DSize))

	// должно быть в имени, а получаем...10 0 9 53 0 0 0 0 1 0 57 2
	// qqq := []byte{0x6f, 0x78, 0x79, 0x67, 0x65, 0x6e, 0x5f, 0x31, 0x36, 0x78, 0x31, 0x36}
	// fmt.Println(string(qqq))
	// fmt.Println(heapBytes[0:12])

	// recordsBuf := bytes.NewBuffer()

	// //--- magic
	// magic, err := ushort2(gr)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// log.Println("magic: ", magic)

	// // magic := make([]byte, 2)
	// // n, err := gr.Read(magic)
	// // if err != nil {
	// // 	log.Fatal(err)
	// // }
	// // log.Println("readed bytes: ", n)
	// // log.Println("readed data: ", magic)

	// // data := binary.LittleEndian.Uint16(magic)
	// // log.Println("magic: ", data)

	// // //--- [version](2)
	// version, err := ushort2(gr)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// log.Println("version: ", version)

	// // 	#--- [header_len](2)
	// headerLen, err := ushort2(gr)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// log.Println("headerLen: ", headerLen)
	// 	header_len = ushort2(fd.read(2))
	// 	print("header_len: ", header_len)

	// 	#--- [header_struct]
	// 	header_data = fd.read(header_len)

}
