package main

import (
	"dcat/internal/logger"
	"dcat/internal/scanner"
	"dcat/internal/stor"
	"flag"
	"fmt"
	"time"
)

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

	records, err := scanner.Scan(scanPath)
	if err != nil {
		panic(err)
	}

	vol := stor.Volume{
		Description: stor.VolumeDescription{
			Name:        nameFlag,
			ScanPath:    scanPath,
			Description: descriptionFlag,
			Created:     time.Now(),
			Icon:        1, // TODO
		},
		Records: records,
	}

	stor.Write(targetPath, vol)

}
