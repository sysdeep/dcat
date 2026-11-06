package fyneui

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

type BottomBar struct {
}

func newButtomBar() *BottomBar {
	return &BottomBar{}
}

func (b *BottomBar) Widget() *fyne.Container {
	labelInfo := widget.NewLabel("Info")

	content := container.NewHBox(labelInfo)

	return content
}
