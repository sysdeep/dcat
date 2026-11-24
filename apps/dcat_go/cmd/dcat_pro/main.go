package main

import (
	"dcat/internal/app/proapp"
	"dcat/internal/logger"
	"dcat/internal/ui/pro"
	"flag"
	"fmt"
	"os"
	"path"

	"gioui.org/app"
	"gioui.org/unit"
)

func main() {

	var storagePath string

	flag.StringVar(&storagePath, "storage", "", "path for storage")

	flag.Parse()

	if storagePath == "" {
		panic(fmt.Errorf("storage - required"))
	}

	log := logger.New()

	storagePath = path.Clean(storagePath)

	application := proapp.NewApp(storagePath, log)

	fmt.Println(application.ReadVolumes())

	// dataset
	// vv, err := stor.Read(volPath)
	// if err != nil {
	// 	panic(err)
	// }

	// vp := state.NewVolumeProvider(&vv)

	// This creates a new application window and starts the UI.
	go func() {
		w := new(app.Window)
		ui := pro.NewUI(w, application, log)
		w.Option(
			app.Title("DCat volume"),
			app.Size(unit.Dp(1024), unit.Dp(768)),
			app.MinSize(unit.Dp(800), unit.Dp(600)),
		)
		if err := ui.Run(w); err != nil {
			log.Error(err.Error())
			os.Exit(1)
		}
		os.Exit(0)
	}()

	// This starts Gio main.
	app.Main()
}
