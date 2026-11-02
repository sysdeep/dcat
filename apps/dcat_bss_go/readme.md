# DCatGo

Проект переосмысление DCat.

Создаёт отдельные записи для указанного источника, хранит их в бинарном виде(что то типа bss).

## Dev

Что работает

- простой пакер\анпакер - обработать ошибки
- простой читатель - обработать ошибки
- простой сканер - обработать ошибки

Что осталось

- gzip
- UI

TODO

- https://github.com/qianniancn/flowui - тут полно готовых компонентов!!!!!
- https://github.com/xmhrnx/giode.git - тоже есть

### Использование gzip

```go
package main

import (
	"compress/gzip"
	"fmt"
	"os"
)

func main() {
	// 1. Создаем обычный файл
	file, err := os.Create("data.txt.gz")
	if err != nil {
		fmt.Println("Ошибка создания файла:", err)
		return
	}
	defer file.Close()

	// 2. Оборачиваем файл в gzip.Writer
	gw := gzip.NewWriter(file)

	// ВАЖНО: gw.Close() нужно вызвать ДО file.Close(),
	// чтобы gzip успел сбросить (flush) оставшиеся биты сжатия и записать контрольную сумму (checksum).
	defer gw.Close()

	// 3. Пишем данные (как в обычный файл)
	_, err = gw.Write([]byte("Привет, этот текст будет сжат в gzip!"))
	if err != nil {
		fmt.Println("Ошибка записи:", err)
		return
	}

	fmt.Println("Файл успешно записан и сжат!")
}

```

```go
package main

import (
	"bytes"
	"compress/gzip"
	"fmt"
)

func main() {
	var compressedBuf bytes.Buffer

	// Создаем gzip-писатель, привязанный к нашему буферу
	gw := gzip.NewWriter(&compressedBuf)

	// Пишем данные
	gw.Write([]byte("Сжимаем строку в бинарный буфер"))

	// Закрываем, чтобы завершить gzip-поток в буфере
	gw.Close()

	// Теперь в compressedBuf.Bytes() лежат готовые сжатые байты архива
	fmt.Printf("Размер сжатых данных: %d байт\n", compressedBuf.Len())
}

```
