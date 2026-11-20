package main

import (
	"dcat/internal/app/proapp"
	"dcat/internal/logger"
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

	scanStart := time.Now()
	records, err := proapp.Scan(scanPath)
	if err != nil {
		panic(err)
	}
	log.Info(fmt.Sprintf("scan: %s", time.Since(scanStart)))
	log.Info(fmt.Sprintf("records: %d", len(records)))

	writeStart := time.Now()
	vol := proapp.Volume{
		Description: proapp.VolumeDescription{
			Name:        nameFlag,
			ScanPath:    scanPath,
			Description: descriptionFlag,
			Created:     time.Now(),
			Icon:        1, // TODO
		},
		Records: records,
	}

	proapp.WriteVolumeFile(targetPath, vol)

	log.Info(fmt.Sprintf("write: %s", time.Since(writeStart)))

	// test read volume only
	readStartDescription := time.Now()
	_, err = proapp.ReadVolumeDescription(targetPath)
	if err != nil {
		panic(err)
	}
	log.Info(fmt.Sprintf("read description: %s", time.Since(readStartDescription)))

	// fmt.Println(result)

	// test read
	readStart := time.Now()
	_, err = proapp.ReadVolumeFile(targetPath)
	if err != nil {
		panic(err)
	}
	log.Info(fmt.Sprintf("read full: %s", time.Since(readStart)))

}
