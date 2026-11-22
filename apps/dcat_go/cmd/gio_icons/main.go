package main

import (
	"fmt"
	"os"

	"gioui.org/app"
	"gioui.org/unit"
)

func main() {

	ui := NewUI()

	// This creates a new application window and starts the UI.
	go func() {
		w := new(app.Window)
		w.Option(
			app.Title("DCat volume"),
			app.Size(unit.Dp(1024), unit.Dp(768)),
			app.MinSize(unit.Dp(800), unit.Dp(600)),
		)
		if err := ui.Run(w); err != nil {
			fmt.Println(err.Error())
			os.Exit(1)
		}
		os.Exit(0)
	}()

	// This starts Gio main.
	app.Main()
}
