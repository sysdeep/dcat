package main

import (
	"dcat/internal/bss"
	"dcat/internal/scanner"
	"dcat/internal/stor"
	"fmt"
	"time"
)

func main() {

	records, err := scanner.Scan("/tmp")
	if err != nil {
		panic(err)
	}

	model := stor.Volume{
		Description: stor.VolumeDescription{
			Name:        "Simple сканирование",
			ScanPath:    "/bin",
			Description: "Description",
			Created:     time.Now(),
			Icon:        1,
		},
		Records: records,
		// Records: []stor.FileRecord{
		// 	{ID: 1, ParentID: 0, Name: "file1", Size: 10},
		// 	{ID: 2, ParentID: 0, Name: "file2", Size: 10},
		// 	{ID: 3, ParentID: 0, Name: "file3", Size: 10},
		// },
	}

	fmt.Println(model)
	stor.Write("/tmp/db1", model)

	vv, err := stor.Read("/tmp/db1")
	if err != nil {
		panic(err)
	}
	fmt.Println(vv)
}
func main_1() {

	model := stor.Volume{
		Description: stor.VolumeDescription{
			Name:        "Simple сканирование",
			ScanPath:    "/bin",
			Description: "Description",
			Created:     time.Now(),
			Icon:        1,
		},
		Records: []stor.FileRecord{
			{ID: 1, ParentID: 0, Name: "file1", Size: 10},
			{ID: 2, ParentID: 0, Name: "file2", Size: 10},
			{ID: 3, ParentID: 0, Name: "file3", Size: 10},
		},
	}

	bb, err := bss.Pack(stor.ToBSS(model))
	if err != nil {
		panic(err)
	}

	fmt.Printf("%x\n", bb.Bytes()) // Выведет: 000400000500

	// read
	v, err := bss.Unpack(bb.Bytes())
	if err != nil {
		panic(err)
	}
	fmt.Println(v)
}
