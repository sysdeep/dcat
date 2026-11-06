package fyneui

import (
	"dcat/internal/app/mvsapp"
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

/*

db_path | db_version

*/

type BottomBar struct {
	app *mvsapp.MvsApp

	labelPath    *widget.Label
	labelVersion *widget.Label
}

func newBottomBar(app *mvsapp.MvsApp) *BottomBar {
	b := BottomBar{
		app:          app,
		labelPath:    widget.NewLabel("PATH"),
		labelVersion: widget.NewLabel("VERSION"),
	}

	app.Connect(mvsapp.EvOpened, b.onDatabaseOpened)
	return &b
}

func (b *BottomBar) Widget() *fyne.Container {

	content := container.NewHBox(b.labelPath, b.labelVersion)

	return content
}

func (b *BottomBar) onDatabaseOpened() error {
	// TODO: get system info
	sysInfo, err := b.app.GetSystemInfo()
	if err != nil {
		b.labelPath.SetText(err.Error())
		return err
	}

	b.labelPath.SetText(fmt.Sprintf("DB: %s", sysInfo.DBPath))
	b.labelVersion.SetText(fmt.Sprintf("v: %s", sysInfo.Version))
	return nil
}
