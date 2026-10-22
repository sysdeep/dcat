package logger

import (
	"log/slog"
	"os"

	"github.com/lmittmann/tint"
)

func New() *slog.Logger {
	// NOTE: default text handler
	// h := slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug})

	// NOTE: custom handler
	h := tint.NewTextHandler(os.Stdout, &tint.Options{Level: slog.LevelDebug})
	return slog.New(h)
}
