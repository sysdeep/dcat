package ddselect

import (
	"image"
	"image/color"

	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/op/clip"
	"gioui.org/op/paint"
	"gioui.org/unit"
	"gioui.org/widget"
	"gioui.org/widget/material"
)

// NOTE: только прототип сгенерённый нейронкой
type DDSelect struct {
	Options  []string
	Selected int
	Open     bool

	btn      widget.Clickable
	itemBtns []widget.Clickable
	list     widget.List
}

func NewDDSelect(options []string) *DDSelect {
	return &DDSelect{
		Options:  options,
		itemBtns: make([]widget.Clickable, len(options)),
		list:     widget.List{List: layout.List{Axis: layout.Vertical}},
	}
}

func (s *DDSelect) Layout(gtx layout.Context, th *material.Theme) layout.Dimensions {
	// 1. Обрабатываем клик по основной кнопке
	for s.btn.Clicked(gtx) {
		s.Open = !s.Open
	}

	// 2. Обрабатываем выбор элемента списка
	for i := range s.itemBtns {
		for s.itemBtns[i].Clicked(gtx) {
			s.Selected = i
			s.Open = false
		}
	}

	// 3. Рисуем саму кнопку (закрытое состояние)
	selectedText := "Выберите..."
	if s.Selected >= 0 && s.Selected < len(s.Options) {
		selectedText = s.Options[s.Selected]
	}

	dims := widget.Border{
		Color:        color.NRGBA{R: 180, G: 180, B: 180, A: 255},
		CornerRadius: unit.Dp(4),
		Width:        unit.Dp(1),
	}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		return s.btn.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
			return layout.UniformInset(unit.Dp(10)).Layout(gtx, func(gtx layout.Context) layout.Dimensions {
				return layout.Flex{Alignment: layout.Middle, Spacing: layout.SpaceBetween}.Layout(gtx,
					layout.Rigid(material.Body1(th, selectedText).Layout),
					layout.Rigid(material.Body1(th, "▼").Layout),
				)
			})
		})
	})

	// 4. Если список открыт — откладываем его отрисовку поверх всего интерфейса
	if s.Open {
		macro := op.Record(gtx.Ops)
		// Сдвигаем список ровно под кнопку (по оси Y на dims.Size.Y)
		op.Offset(image.Pt(0, dims.Size.Y+gtx.Dp(2))).Add(gtx.Ops)

		// Ограничиваем ширину списка шириной кнопки, а высоту — максимумом (например, 200dp)
		dropGtx := gtx
		dropGtx.Constraints.Min.X = dims.Size.X
		dropGtx.Constraints.Max.X = dims.Size.X
		dropGtx.Constraints.Max.Y = gtx.Dp(200)

		s.layoutDropdown(dropGtx, th)
		call := macro.Stop()
		op.Defer(gtx.Ops, call)
	}

	return dims
}

func (s *DDSelect) layoutDropdown(gtx layout.Context, th *material.Theme) layout.Dimensions {
	return widget.Border{
		Color:        color.NRGBA{R: 180, G: 180, B: 180, A: 255},
		CornerRadius: unit.Dp(4),
		Width:        unit.Dp(1),
	}.Layout(gtx, func(gtx layout.Context) layout.Dimensions {
		// Фон выпадающего списка
		return layout.Stack{}.Layout(gtx,
			layout.Expanded(func(gtx layout.Context) layout.Dimensions {
				paint.FillShape(gtx.Ops, color.NRGBA{R: 255, G: 255, B: 255, A: 255}, clip.Rect{Max: gtx.Constraints.Min}.Op())
				return layout.Dimensions{Size: gtx.Constraints.Min}
			}),
			layout.Stacked(func(gtx layout.Context) layout.Dimensions {
				return material.List(th, &s.list).Layout(gtx, len(s.Options), func(gtx layout.Context, i int) layout.Dimensions {
					return s.itemBtns[i].Layout(gtx, func(gtx layout.Context) layout.Dimensions {
						// Подсветка при наведении
						if s.itemBtns[i].Hovered() {
							paint.FillShape(gtx.Ops, color.NRGBA{R: 240, G: 240, B: 240, A: 255}, clip.Rect{Max: gtx.Constraints.Max}.Op())
						}
						return layout.UniformInset(unit.Dp(10)).Layout(gtx, material.Body1(th, s.Options[i]).Layout)
					})
				})
			}),
		)
	})
}
