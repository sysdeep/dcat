package rc

import (
	"dcat/assets"

	"gioui.org/op/paint"
)

var FileTypeImagesMap map[int]paint.ImageOp = map[int]paint.ImageOp{
	1:   paint.NewImageOp(assets.MustImage("ftypes/folder.png")),  // folder
	2:   paint.NewImageOp(assets.MustImage("ftypes/empty.png")),   // file
	100: paint.NewImageOp(assets.MustImage("ftypes/unknown.png")), // unknown
}

const FileTypeUnknown = 100

var VolumeImagesMap map[int]paint.ImageOp = map[int]paint.ImageOp{
	1:  paint.NewImageOp(assets.MustImage("volumes/cdwriter_unmount.png")),    // cd
	2:  paint.NewImageOp(assets.MustImage("volumes/dvd_unmount.png")),         // dvd
	3:  paint.NewImageOp(assets.MustImage("volumes/bd_rom.png")),              // bdrom
	4:  paint.NewImageOp(assets.MustImage("volumes/decrypted.png")),           // crypted
	5:  paint.NewImageOp(assets.MustImage("volumes/user_home.png")),           // folder
	6:  paint.NewImageOp(assets.MustImage("volumes/cdaudio_unmount.png")),     // audio_cd
	7:  paint.NewImageOp(assets.MustImage("volumes/hdd_unmount.png")),         // hdd
	8:  paint.NewImageOp(assets.MustImage("volumes/hdd_usb_unmount.png")),     // hdd_usb
	9:  paint.NewImageOp(assets.MustImage("volumes/usbpendrive_unmount.png")), // flash
	10: paint.NewImageOp(assets.MustImage("volumes/sd_mmc_unmount.png")),      // sd
	11: paint.NewImageOp(assets.MustImage("volumes/document_save.png")),       // floppy
	12: paint.NewImageOp(assets.MustImage("volumes/nfs_unmount.png")),         // net
	13: paint.NewImageOp(assets.MustImage("volumes/media_tape.png")),          // tape
	14: paint.NewImageOp(assets.MustImage("volumes/unknown.png")),             // other
}

const VolumeUnknown = 14
