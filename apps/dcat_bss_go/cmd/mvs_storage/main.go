package main

import (
	"dcat/internal/storages/mvs"
	"fmt"
	"time"
)

func main() {

	dbPath := "/home/igor/1.gcat"

	st, err := mvs.NewMVS(dbPath)
	if err != nil {
		panic(err)
	}

	volumes, err := st.GetVolumes()
	if err != nil {
		panic(err)
	}

	for _, v := range volumes {
		fmt.Printf("%s - %s - %s - %s\n", v.UUID, v.Name, v.Created.Format(time.DateTime), v.Updated.Format(time.DateTime))
	}

}
