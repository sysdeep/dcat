package fyneui

import (
	"dcat/internal/app/state"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

type Navigation struct {
	vp *state.VolumeProvider
	as *AppState

	stackContainer *fyne.Container
}

func newNavigation(vp *state.VolumeProvider, as *AppState) *Navigation {
	n := Navigation{
		vp:             vp,
		as:             as,
		stackContainer: container.NewHBox(),
	}

	as.Connect(AppStateStackChanged, n.onStack)

	return &n
}

func (n *Navigation) Widget() *fyne.Container {

	btnHome := widget.NewButton("Home", func() {
		n.as.GoHome()
	})

	btnBack := widget.NewButton("Back", func() {
		n.as.GoBack()
	})

	topBarContainer := container.NewHBox(btnHome, btnBack, layout.NewSpacer(), n.stackContainer, layout.NewSpacer(), layout.NewSpacer())

	return topBarContainer

}

func (n *Navigation) onStack() error {

	objects := []fyne.CanvasObject{}
	for i, ff := range n.as.FoldersStack {
		objects = append(objects, widget.NewButton(ff.Name, func() {
			n.as.GoInStack(i + 1)
		}))
	}

	n.stackContainer.Objects = objects

	return nil
}
