package main

import (
	"dcat/internal/stor"
	"dcat/internal/ui/gioui"
	"flag"
	"fmt"
	"log"
	"os"

	"gioui.org/app"
	"gioui.org/unit"
)

func main() {

	var volPath string

	flag.StringVar(&volPath, "volume", "", "path for volume")

	flag.Parse()

	if volPath == "" {
		panic(fmt.Errorf("volume - required"))
	}

	// dataset
	vv, err := stor.Read(volPath)
	if err != nil {
		panic(err)
	}

	vp := gioui.NewVolumeProvider(&vv)

	ui := gioui.NewUI(vp)

	// This creates a new application window and starts the UI.
	go func() {
		w := new(app.Window)
		w.Option(
			app.Title("DCat volume"),
			app.Size(unit.Dp(1024), unit.Dp(768)),
			app.MinSize(unit.Dp(800), unit.Dp(600)),
		)
		if err := ui.Run(w); err != nil {
			log.Println(err)
			os.Exit(1)
		}
		os.Exit(0)
	}()

	// This starts Gio main.
	app.Main()

}
