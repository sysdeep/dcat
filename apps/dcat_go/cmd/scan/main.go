package main

import (
	"dcat/internal/scanner"
	"fmt"
)

func main() {

	items, err := scanner.Scan("/tmp")
	if err != nil {
		panic(err)
	}

	for _, it := range items {
		fmt.Println(it.Name, it.ID, it.Path)
	}
}
