package main

import (
	"dcat/internal/logger"
	"dcat/internal/storages/mvsv2"
	"flag"
	"fmt"
	"time"
)

/*
bssv2 - на 400_000 файлов достаточно ощутимая задержка в 300ms
предлагаю провести эксперимент с sqlite

#### sqlite

400_000

- создание
  - холодный старт - 15 сек
  - кеш диска - 4 сек

- размер 29Мб

2_000_000

- размер - 114Мб

#### bbsv2

400_000

- создание
  - 2 на сканирование + 1 на запись = 3 сек

- размер 3.5Мб

#### выводы

с оптимизацие по типам в sqlite всё равно значительный пройгрыш по размеру
по скорости, sqlite с транзакцией сопоставим с вариантом bbs
дальнейших замеров нет смысла делать...
хотя интересно как будет вести себя выборка на большой базе....

для наполнения можно запускать данный бинарник несколько раз
*/
func main() {

	var scanPath string
	var targetPath string
	var nameFlag string
	var descriptionFlag string

	flag.StringVar(&scanPath, "scan-path", "", "")
	flag.StringVar(&targetPath, "target-path", "", "")
	flag.StringVar(&nameFlag, "name", "", "")
	flag.StringVar(&descriptionFlag, "description", "", "optional")

	flag.Parse()

	if scanPath == "" {
		panic(fmt.Errorf("scan path: required"))
	}

	if targetPath == "" {
		panic(fmt.Errorf("target path: required"))
	}

	if nameFlag == "" {
		panic(fmt.Errorf("volume name: required"))
	}

	log := logger.New()
	log.Info("start scan: " + scanPath + " -> " + targetPath)

	mv, err := mvsv2.NewMVSv2(targetPath)
	if err != nil {
		panic(err)
	}

	scanStart := time.Now()
	err = Scan(scanPath, mv)
	if err != nil {
		panic(err)
	}

	log.Info(fmt.Sprintf("scan: %s", time.Since(scanStart)))

}
