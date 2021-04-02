package main

import "fmt"

type Heap struct {
	b []byte
}

func NewHeap(data []byte) *Heap {
	h := &Heap{
		b: data,
	}
	return h
}

func (h *Heap) GetString(pos uint32, size uint16) string {
	bb := h.b[pos : pos+uint32(size)]
	fmt.Println(bb)
	return string(bb)
}
