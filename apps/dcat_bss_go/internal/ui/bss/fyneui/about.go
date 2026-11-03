package fyneui

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func makeAbout() *fyne.Container {
	labelInfo := widget.NewLabel("About")

	content := container.NewHBox(labelInfo)

	return content
}
