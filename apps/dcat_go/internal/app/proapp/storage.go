package proapp

import (
	"compress/gzip"
	"dcat/internal/bssv2"
	"os"
)

func ReadVolumeFile(filePath string) (Volume, error) {

	file, err := os.Open(filePath)
	if err != nil {
		return Volume{}, err
	}
	defer file.Close()

	// 2. Создаем gzip-ридер поверх открытого файла
	gzipReader, err := gzip.NewReader(file)
	if err != nil {
		return Volume{}, err
	}
	defer gzipReader.Close()

	bssVolume, err := bssv2.Unpack(gzipReader)
	if err != nil {
		return Volume{}, err
	}

	return fromBBSVolume(bssVolume, filePath), nil
}

func ReadVolumeDescription(filePath string) (VolumeDescription, error) {

	file, err := os.Open(filePath)
	if err != nil {
		return VolumeDescription{}, err
	}
	defer file.Close()

	// 2. Создаем gzip-ридер поверх открытого файла
	gzipReader, err := gzip.NewReader(file)
	if err != nil {
		return VolumeDescription{}, err
	}
	defer gzipReader.Close()

	bssVolumeDescription, err := bssv2.UnpackDescription(gzipReader)
	if err != nil {
		return VolumeDescription{}, err
	}

	return fromBSSVolumeDescription(bssVolumeDescription, filePath), nil
}

func WriteVolumeFile(filePath string, vol Volume) error {
	bssVolume := toBSS(vol)

	// NOTE: без сжатия
	// return os.WriteFile(filePath, buf.Bytes(), 0o666)

	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	// 2. Оборачиваем файл в gzip.Writer
	gw := gzip.NewWriter(file)
	defer gw.Close()

	return bssv2.Pack(&bssVolume, gw)
}
