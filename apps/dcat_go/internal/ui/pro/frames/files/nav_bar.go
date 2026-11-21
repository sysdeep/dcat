package files

import (
	"dcat/internal/ui/pro/appstate"

	"gioui.org/layout"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type NavBar struct {
	th       *material.Theme
	appState *appstate.AppState

	homeButton widget.Clickable
	backButton widget.Clickable

	stackView    *material.ListStyle
	stackButtons []widget.Clickable
}

func NewNavBar(th *material.Theme, appState *appstate.AppState) *NavBar {
	var stackState widget.List

	stackView := material.List(th, &stackState)

	return &NavBar{
		th:           th,
		appState:     appState,
		stackView:    &stackView,
		stackButtons: make([]widget.Clickable, 0),
	}
}

func (nb *NavBar) Layout(gtx C) D {

	if nb.backButton.Clicked(gtx) {
		nb.appState.PopFolder()
	}

	if nb.homeButton.Clicked(gtx) {
		nb.appState.DropStack()
	}

	if len(nb.stackButtons) < len(nb.appState.StackFiles) {
		need := len(nb.appState.StackFiles) - len(nb.stackButtons)
		nb.stackButtons = append(nb.stackButtons, make([]widget.Clickable, need)...)
	}

	return layout.Flex{Axis: layout.Horizontal}.Layout(gtx,

		layout.Rigid(material.Button(nb.th, &nb.homeButton, "H").Layout),
		layout.Rigid(layout.Spacer{Width: 2}.Layout),
		layout.Rigid(material.Button(nb.th, &nb.backButton, "B").Layout),

		layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
		layout.Rigid(func(gtx layout.Context) layout.Dimensions {

			stackItems := nb.appState.StackFiles

			return nb.stackView.Layout(gtx, len(stackItems), func(gtx layout.Context, i int) layout.Dimensions {

				if nb.stackButtons[i].Clicked(gtx) {
					nb.appState.GoToStack(i)
				}
				return layout.Inset{Left: 1, Right: 1}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
					return material.Button(nb.th, &nb.stackButtons[i], stackItems[i].Name).Layout(gtx)
				})
			})
		}),
	)

}
