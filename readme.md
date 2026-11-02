# DCat

Проект предназначен для сохранения структуры каталога или диска в локальной базе данных с последующим просмотром и навигацией.
Является представителем программ - каталогизаторов.

## Другие проекты и ответвления

- [JDCat](https://github.com/sysdeep/jdcat) - проект на Qt с базой в виде json
- [QDCat](https://gitlab.com/sysdeep/qdcat) - проект на Qt с поддержкой оригинального хранилища dcat

## Требования

- python 3.12
- tkinter
- sqlite3

## Dev

- 8 - python3 -m add.AppBss.main
- 10 - python3 -m add.features.10_binmap.viewer.main

## Perf

| Application | mem   | cpu |
| ----------- | ----- | --- |
| Dcat        | 139mb |     |
| QDcat       | 100mb | 0%  |
| dcat_go     | 44mb  | 0%  |
| imcat       | 100mb | 8%  |


