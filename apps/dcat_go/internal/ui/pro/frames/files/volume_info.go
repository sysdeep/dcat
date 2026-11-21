package files

import (
	"dcat/internal/ui/pro/appstate"
	"fmt"
	"image/color"

	"gioui.org/layout"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

type VolumeInfo struct {
	th       *material.Theme
	appState *appstate.AppState
}

func NewVolumeInfo(th *material.Theme, appState *appstate.AppState) *VolumeInfo {
	return &VolumeInfo{
		th:       th,
		appState: appState,
	}
}

func (vi *VolumeInfo) Layout(gtx C) D {
	if vi.appState.CurrentVolume == nil {
		return layout.Dimensions{}
	}

	return widget.Border{Color: color.NRGBA{R: 200, B: 200, G: 200, A: 250}, Width: unit.Dp(0.8), CornerRadius: unit.Dp(5)}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		return layout.Flex{Axis: layout.Horizontal}.Layout(gtx,
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
					layout.Rigid(material.Body1(vi.th, fmt.Sprintf("records: %d", len(vi.appState.CurrentVolume.Records))).Layout),
					layout.Rigid(material.Body1(vi.th, fmt.Sprintf("file: %s", vi.appState.CurrentVolume.Description.FilePath)).Layout),
				)
			}),
			layout.Rigid(layout.Spacer{Width: defaultMargin}.Layout),
			layout.Rigid(func(gtx layout.Context) layout.Dimensions {
				return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
					layout.Rigid(material.Body1(vi.th, fmt.Sprintf("created: %s", vi.appState.CurrentVolume.Description.Created.String())).Layout),
					layout.Rigid(material.Body1(vi.th, fmt.Sprintf("icon: %d", vi.appState.CurrentVolume.Description.Icon)).Layout),
				)
			}),
		)
	})

}
