package assets

import (
	"embed"
	"image"
	_ "image/png"
)

//go:embed *
var assets embed.FS

func LoadImage(name string) (image.Image, error) {
	f, err := assets.Open(name)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	img, _, err := image.Decode(f)
	if err != nil {
		return nil, err
	}

	return img, nil
}

func MustImage(name string) image.Image {
	f, err := assets.Open(name)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	img, _, err := image.Decode(f)
	if err != nil {
		panic(err)
	}

	return img
}
