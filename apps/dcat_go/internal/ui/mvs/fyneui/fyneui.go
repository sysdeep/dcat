package fyneui

import (
	"dcat/internal/app/mvsapp"
	"dcat/internal/app/state"
	"fmt"
	"image/color"
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

// type FyneUI struct{}

func NewFyneUI(vp *state.VolumeProvider, mvsApp *mvsapp.MvsApp) {
	a := app.New()

	// Оборачиваем дефолтную тему и устанавливаем её в настройки приложения
	myTheme := forcedLightTheme{Theme: theme.DefaultTheme()}
	a.Settings().SetTheme(myTheme)

	// window
	w := a.NewWindow("DCat fyne example")
	w.Resize(fyne.NewSize(1024, 768))

	appState := newAppState(mvsApp)

	// components
	navBar := newNavigation(vp, appState)
	filesList := NewFilesList(appState)
	bottomBar := newBottomBar(mvsApp)
	volumesList := newVolumesList(appState)

	exampleBase := "/home/igor/1.gcat"
	topB := container.NewVBox(
		container.NewHBox(

			widget.NewLabel(exampleBase),
			widget.NewButton("open", func() {
				err := mvsApp.Open(exampleBase)
				if err != nil {
					fmt.Println(err)
				} else {

				}
			}),
		),
		navBar.Widget(),
	)

	// layout
	content := container.NewBorder(topB, bottomBar.Widget(), volumesList.Widget(), nil, filesList.Widget())
	w.SetContent(content) // output,

	// main menu
	m := fyne.NewMainMenu(
		fyne.NewMenu("File", fyne.NewMenuItem("Show", func() {
			log.Println("Tapped show")
		})),
		fyne.NewMenu("About", fyne.NewMenuItem("Show", func() {
			log.Println("Tapped show")

			// NOTE: возможно его надо создавать единожды?
			d := dialog.NewCustom("Title about", "dimiss", makeAbout(), w)
			d.Show()

		})),
	)
	w.SetMainMenu(m)

	w.Show()

	a.Run()
}

//----------------

// Создаем свою структуру для принудительной светлой темы
type forcedLightTheme struct {
	fyne.Theme
}

// Переопределяем метод Color
func (f forcedLightTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
	// Игнорируем переданный системой 'variant' и всегда запрашиваем VariantLight
	return f.Theme.Color(name, theme.VariantLight)
}
