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

	tableBytes := make([]byte, vh.TableLength)
	_, err = gr.Read(tableBytes)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("records calculated: ", len(tableBytes)/40)

	heapBytes := make([]byte, vh.HeapLength)
	_, err = gr.Read(heapBytes)
	if err != nil {
		log.Fatal(err)
	}

	heap := NewHeap(heapBytes)

	log.Println(heap.GetString(vh.NPos, vh.NSize)) // должно быть... b'6f787967656e5f3136783136' а есть: 10 0 9 53 0 0 0 0 1 0 57 2
	log.Println(heap.GetString(vh.PPos, vh.PSize))

	// должно быть в имени, а получаем...10 0 9 53 0 0 0 0 1 0 57 2
	qqq := []byte{0x6f, 0x78, 0x79, 0x67, 0x65, 0x6e, 0x5f, 0x31, 0x36, 0x78, 0x31, 0x36}
	fmt.Println(string(qqq))
	fmt.Println(heapBytes[0:12])

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
