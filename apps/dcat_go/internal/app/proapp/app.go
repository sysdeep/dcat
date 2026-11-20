package proapp

import (
	"log/slog"
	"os"
	"path/filepath"
)

type App struct {
	StoragePath string
	log         *slog.Logger
}

func NewApp(storagePath string, log *slog.Logger) *App {
	return &App{
		StoragePath: storagePath,
		log:         log,
	}
}

func (app *App) ReadVolumes() ([]VolumeDescription, error) {
	result := make([]VolumeDescription, 0)

	entries, err := os.ReadDir(app.StoragePath)
	if err != nil {
		return result, err
	}

	for _, entry := range entries {

		if entry.IsDir() {
			continue
		}
		fullPath := filepath.Join(app.StoragePath, entry.Name())

		app.log.Debug("read file: " + fullPath)
		vd, err := ReadVolumeDescription(fullPath)
		if err != nil {
			return result, err
		}
		result = append(result, vd)
	}

	return result, nil
}

func (app *App) ReadVolume(filePath string) (Volume, error) {
	return ReadVolumeFile(filePath)
}
