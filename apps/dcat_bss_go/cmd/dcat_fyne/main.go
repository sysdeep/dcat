package main

import (
	"dcat/internal/app/mvsapp"
	"dcat/internal/app/state"
	"dcat/internal/stor"
	"dcat/internal/ui/mvs/fyneui"
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
	mvsApp := mvsapp.NewMvsApp()

	fyneui.NewFyneUI(vp, mvsApp)
}
