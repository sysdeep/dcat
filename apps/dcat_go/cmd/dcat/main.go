package main

import (
	"image/color"
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

// Создаем свою структуру для принудительной светлой темы
type forcedLightTheme struct {
	fyne.Theme
}

// Переопределяем метод Color
func (f forcedLightTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
	// Игнорируем переданный системой 'variant' и всегда запрашиваем VariantLight
	return f.Theme.Color(name, theme.VariantLight)
}

func main() {
	a := app.New()
	// a.Settings().SetTheme(theme.DefaultTheme())
	// a.Settings().SetTheme()

	// Оборачиваем дефолтную тему и устанавливаем её в настройки приложения
	myTheme := forcedLightTheme{Theme: theme.DefaultTheme()}
	a.Settings().SetTheme(myTheme)

	w := a.NewWindow("Hello World")

	var data = []string{"a", "string", "list"}
	list := widget.NewList(
		func() int {
			return len(data)
		},
		func() fyne.CanvasObject {
			return widget.NewLabel("template")
		},
		func(i widget.ListItemID, o fyne.CanvasObject) {
			o.(*widget.Label).SetText(data[i])
		})

	tabs := container.NewAppTabs(
		container.NewTabItem("List", list),
		container.NewTabItem("Tab 1", widget.NewLabel("Hello")),
		container.NewTabItem("Tab 2", widget.NewLabel("World!")),
	)

	// // tree
	// tree := widget.NewTree(
	// 	func(id widget.TreeNodeID) []widget.TreeNodeID {
	// 		switch id {
	// 		case "":
	// 			return []widget.TreeNodeID{"a", "b", "c"}
	// 		case "a":
	// 			return []widget.TreeNodeID{"a1", "a2"}
	// 		}
	// 		return []string{}
	// 	},
	// 	func(id widget.TreeNodeID) bool {
	// 		return id == "" || id == "a"
	// 	},
	// 	func(branch bool) fyne.CanvasObject {
	// 		if branch {
	// 			return widget.NewLabel("Branch template")
	// 		}
	// 		return widget.NewLabel("Leaf template")
	// 	},
	// 	func(id widget.TreeNodeID, branch bool, o fyne.CanvasObject) {
	// 		text := id
	// 		if branch {
	// 			text += " (branch)"
	// 		}
	// 		o.(*widget.Label).SetText(text)
	// 	})

	// w.SetContent(widget.NewLabel("Hello World!"))
	// message := widget.NewLabel("Welcome")
	// button := widget.NewButton("Update", func() {
	// 	formatted := time.Now().Format("Time: 03:04:05")
	// 	message.SetText(formatted)

	// })

	vl := NewVolumesList()
	dl := NewVolumesList()

	leftBar := container.NewGridWithRows(2, vl.Widget(), dl.Widget()) //  widget.NewLabel("left 1"), widget.NewLabel("left 2"), tree,

	filesList := NewFilesList()
	// 3. ОБЕРТКА ДЛЯ ШИРИНЫ: задаем желаемую ширину (например, 200px)
	// Высоту ставим 0 или 1 — Border всё равно её переопределит и растянет по вертикали.
	// leftBarResized := container.NewGridWrap(fyne.NewSize(200, 1), leftBar)

	// output := canvas.NewText(time.Now().Format(time.TimeOnly), color.NRGBA{G: 0xff, A: 0xff})
	// output.TextStyle.Monospace = true
	// output.TextSize = 32
	topBar := canvas.NewText("topBar", color.Black)
	bottomBar := canvas.NewText("bottomBar", color.Black)
	// middle := canvas.NewText("content", color.Black)
	content := container.NewBorder(topBar, bottomBar, leftBar, tabs, filesList.Widget())
	// w.SetContent(container.NewHBox(tree, tabs)) // output,
	w.SetContent(content) // output,
	// w.SetContent(tabs)
	// go func() {
	// 	ticker := time.NewTicker(time.Second)
	// 	for range ticker.C {
	// 		fyne.Do(func() {
	// 			output.Text = time.Now().Format(time.TimeOnly)
	// 			output.Refresh()
	// 		})
	// 	}
	// }()

	m := fyne.NewMainMenu(
		fyne.NewMenu("File", fyne.NewMenuItem("Show", func() {
			log.Println("Tapped show")
		})),
		fyne.NewMenu("About", fyne.NewMenuItem("Show", func() {
			log.Println("Tapped show")
		})),
	)
	w.SetMainMenu(m)

	w.Show()

	// w2 := a.NewWindow("Larger")
	// // w2.SetContent(widget.NewLabel("More content"))
	// w2.SetContent(widget.NewButton("Open new", func() {
	// 	w3 := a.NewWindow("Third")
	// 	w3.SetContent(widget.NewLabel("Third"))
	// 	w3.Show()
	// }))
	// w2.Resize(fyne.NewSize(100, 100))
	// w2.Show()

	a.Run()
}
