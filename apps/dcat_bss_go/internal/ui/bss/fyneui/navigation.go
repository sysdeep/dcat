package fyneui

import (
	"dcat/internal/app/state"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

type Navigation struct {
	vp *state.VolumeProvider
}

func newNavigation(vp *state.VolumeProvider) *Navigation {
	return &Navigation{
		vp: vp,
	}
}

func (n *Navigation) Widget() *fyne.Container {

	btnHome := widget.NewButton("Home", func() {
		n.vp.PushPath(1)
	})

	btnBack := widget.NewButton("Back", func() {
		if !n.vp.PathIsEmpty() {
			n.vp.PopPath()
		}
	})

	topBarContainer := container.NewHBox(btnHome, btnBack)

	return topBarContainer

}
