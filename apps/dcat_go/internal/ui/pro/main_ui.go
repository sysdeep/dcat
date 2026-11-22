package pro

import (
	"dcat/internal/ui/pro/appstate"
	"dcat/internal/ui/pro/frames/files"
	"dcat/internal/ui/pro/frames/statusbar"
	"dcat/internal/ui/pro/frames/toolbar"
	"dcat/internal/ui/pro/frames/volumes"

	"gioui.org/layout"
	"gioui.org/widget/material"
)

type MainUI struct {
	th *material.Theme

	// frames
	volumesFrame   *volumes.Volumes
	filesFrame     *files.Files
	toolbarFrame   *toolbar.Toolbar
	statusbarFrame *statusbar.Statusbar
}

func newMainUI(th *material.Theme, appState *appstate.AppState) *MainUI {
	return &MainUI{
		th:             th,
		volumesFrame:   volumes.NewVolumes(th, appState),
		filesFrame:     files.NewFiles(th, appState),
		toolbarFrame:   toolbar.NewToolbar(th, appState),
		statusbarFrame: statusbar.NewStatusbar(th, appState),
	}
}

func (mui *MainUI) Layout(gtx C) D {

	return layout.Flex{Axis: layout.Vertical}.Layout(gtx,
		// toolbar
		layout.Rigid(mui.toolbarFrame.Layout),

		// central
		layout.Flexed(1, func(c C) D {
			return layout.Flex{Axis: layout.Horizontal}.Layout(c,
				layout.Flexed(3, mui.volumesFrame.Layout),
				layout.Flexed(10, mui.filesFrame.Layout),
			)
		}),

		// status bar
		layout.Rigid(mui.statusbarFrame.Layout),
	)
}
