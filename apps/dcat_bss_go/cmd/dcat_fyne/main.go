package main

import (
	"dcat/internal/app/state"
	"dcat/internal/stor"
	"dcat/internal/ui/fyneui"
	"flag"
	"fmt"
)

func main() {

	var volPath string

	flag.StringVar(&volPath, "volume", "", "path for volume")

	flag.Parse()

	if volPath == "" {
		panic(fmt.Errorf("volume - required"))
	}

	vv, err := stor.Read(volPath)
	if err != nil {
		panic(err)
	}

	vp := state.NewVolumeProvider(&vv)

	fyneui.NewFyneUI(vp)
}
