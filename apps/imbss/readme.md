# ImCalendar

Маленький простой календарик для использования совместно с тайловыми VM как замена ушедшему gsimplecal.

- отображение сетки на месяц
- перемотка по месяцам и годам

![v 1.0.0](https://github.com/sysdeep/play_cpp/raw/master/projects/imcalendar/img/imcalendar_v1.0.0.png)

## TODO

- [x] BUG ноябрь 2026 - 31 число отображается в субботу, хотя 31 вообще нет
- [x] подсветить выходные
- [x] добавить сочетание клавиш для выхода, например q или Esq
- [x] добавить about
- [ ] сетка 7x5 - в пустые клетки добавить отображение пред-след месяца - заблокированные
- [x] аргументы cmd - version
- [x] добавить шрифт в ресурсы
- [x] добавить кнопку today
- [x] дефект - разные месяцы содержат разное кол-во строк -> скачки то что ниже сетки

## Dev

- https://howardhinnant.github.io/date/date.html

### argparse

https://github.com/p-ranav/argparse

##№ Fonts

```bash
g++ misc/fonts/binary_to_compressed_c.cpp -o binary_to_compressed_c

./binary_to_compressed_c ../vendors/imgui/misc/fonts/Roboto-Medium.ttf Roboto > roboto.cpp
./binary_to_compressed_c ../vendors/fonts/JetBrainsMonoNerdFontMono-Regular.ttf JetBrains > ../src/ui/gen/font.cpp
```

### Integration in ImGui

Once the tool has generated the C-style array in your source file, you can load the data in your C++ application using the ImGui functions designed for embedded, compressed data. A common function is `ImGui::GetIO().Fonts->AddFontFromMemoryCompressedTTF()` or `AddFontFromMemoryCompressedBase85TTF()`, depending on the flags used during generation

TODO: - добавить рекомпеляцию в make

1 - поместить нужный шрифт в vendors/fonts/
2 - скомпилировать `./binary_to_compressed_c ../vendors/fonts/JetBrainsMonoNerdFontMono-Regular.ttf JetBrains > ../src/ui/gen/font_FONTNAME.cpp`
3 - подключить в main_window `io->Fonts->AddFontFromMemoryCompressedTTF(JetBrains_compressed_data, JetBrains_compressed_size);`

### Version

Для подстановки версии используется функционал CMake.

1 - определить версию `project(imcalculator VERSION 0.0.2 LANGUAGES CXX)`

2 - создать файл-шаблон который будет потом заполнен cmake - см. version.hpp.in

3 - задать правила подстановки, берём шаблон и рендерим в папку сборки

```cmake
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/src/version.hpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/version.hpp"
)
```

4 - добавить папку сборки в пути поиска

```cmake
target_include_directories(${APP_TARGET} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")
```

5 - подключить version.hpp и использовать - `std::cout << "Версия: " << APP_VERSION << std::endl; `
