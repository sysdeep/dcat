package main

import (
	"dcat/internal/stor"
	"dcat/internal/storages/mvsv2"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"time"
)

// версия со сканированием в goroutine и постом в канал для транзакции
func Scan(root string, storage *mvsv2.MVSv2) error {

	// make volume ----------------------------------------
	volume := mvsv2.DBVolume{
		Name:        "example",
		ScanPath:    root,
		Created:     time.Now(),
		Updated:     time.Now(),
		VType:       1,
		Description: "desc",
	}

	volID, err := storage.CreateVolume(volume)
	if err != nil {
		return err
	}

	ch := make(chan mvsv2.DBFile)

	go ScanInternal(root, ch, volID)

	storage.InsertManyMaker(ch)

	return nil
}

func ScanInternal(root string, ch chan mvsv2.DBFile, volID int64) error {

	defer close(ch)

	// check root -----------------------------------------
	root = filepath.Clean(root)

	rootInfo, err := os.Stat(root)
	if err != nil {
		return fmt.Errorf("Error reading directory metadata: %v", err)
	}

	// prepare scan ---------------------------------------
	var idCounter int64 = 1

	// Мапа для связи "Путь к папке -> Числовой ID папки"
	pathToID := make(map[string]int64)

	// 1. Создаем и добавляем корень
	rootItem := mvsv2.DBFile{
		ID:       idCounter,
		ParentID: 0, // У корня нет родителя
		Name:     filepath.Base(root),
		FType:    stor.FTYPE_DIR,
		Size:     0,
		CTime:    rootInfo.ModTime(),
		VolumeID: volID,
	}
	pathToID[root] = idCounter
	idCounter++

	ch <- rootItem
	// _, err = storage.CreateFile(rootItem)
	// if err != nil {
	// 	return err
	// }

	err = filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {

		// Ошибка доступа к файлу/папке (например, нет прав)
		if err != nil {
			// TODO
			//
			// fmt.Printf("Ошибка доступа к %s: %v\n", path, err)
			// return err // Возврат ошибки прервет весь обход
			return nil
		}

		// Пропускаем сам корень, мы его добавили вручную
		if path == root {
			return nil
		}

		// Вычисляем путь родителя
		parentDir := filepath.Dir(path)
		parentID, exists := pathToID[parentDir]
		if !exists {
			return fmt.Errorf("родительский ID не найден для: %s", path)
		}

		ftype := stor.FTYPE_FILE
		if d.IsDir() {
			ftype = stor.FTYPE_DIR
		}

		fileInfo, err := d.Info()
		if err != nil {
			return err
		}

		// Создаем плоский элемент
		item := mvsv2.DBFile{
			ID:       idCounter,
			ParentID: parentID,
			Name:     d.Name(),
			FType:    ftype,
			Size:     fileInfo.Size(),
			CTime:    fileInfo.ModTime(),
		}

		// items = append(items, item)

		ch <- item
		// _, err = storage.CreateFile(item)
		// if err != nil {
		// 	return err
		// }

		// Если это папка, запоминаем её ID для будущих детей
		if d.IsDir() {
			pathToID[path] = idCounter
		}

		// // Проверяем, что это: папка или файл
		// if d.IsDir() {
		// 	fmt.Printf("[Папка] %s\n", path)
		// } else {
		// 	fmt.Printf("[Файл ] %s\n", path)
		// }

		// NOTE: как получить информацию
		// fmt.Println(d.Info())

		idCounter++
		return nil // nil означает "продолжить обход"
	})

	if err != nil {
		return err
	}

	return nil
}

// работает но по одному слишком долго
func ScanSlow(root string, storage *mvsv2.MVSv2) error {

	// check root -----------------------------------------
	root = filepath.Clean(root)

	rootInfo, err := os.Stat(root)
	if err != nil {
		return fmt.Errorf("Error reading directory metadata: %v", err)
	}

	// make volume ----------------------------------------
	volume := mvsv2.DBVolume{
		Name:        "example",
		ScanPath:    root,
		Created:     time.Now(),
		Updated:     time.Now(),
		VType:       1,
		Description: "desc",
	}

	volID, err := storage.CreateVolume(volume)
	if err != nil {
		return err
	}

	// prepare scan ---------------------------------------
	var idCounter int64 = 1

	// Мапа для связи "Путь к папке -> Числовой ID папки"
	pathToID := make(map[string]int64)

	// 1. Создаем и добавляем корень
	rootItem := mvsv2.DBFile{
		ID:       idCounter,
		ParentID: 0, // У корня нет родителя
		Name:     filepath.Base(root),
		FType:    stor.FTYPE_DIR,
		Size:     0,
		CTime:    rootInfo.ModTime(),
		VolumeID: volID,
	}
	pathToID[root] = idCounter
	idCounter++

	_, err = storage.CreateFile(rootItem)
	if err != nil {
		return err
	}

	err = filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {

		// Ошибка доступа к файлу/папке (например, нет прав)
		if err != nil {
			// TODO
			//
			// fmt.Printf("Ошибка доступа к %s: %v\n", path, err)
			// return err // Возврат ошибки прервет весь обход
			return nil
		}

		// Пропускаем сам корень, мы его добавили вручную
		if path == root {
			return nil
		}

		// Вычисляем путь родителя
		parentDir := filepath.Dir(path)
		parentID, exists := pathToID[parentDir]
		if !exists {
			return fmt.Errorf("родительский ID не найден для: %s", path)
		}

		ftype := stor.FTYPE_FILE
		if d.IsDir() {
			ftype = stor.FTYPE_DIR
		}

		fileInfo, err := d.Info()
		if err != nil {
			return err
		}

		// Создаем плоский элемент
		item := mvsv2.DBFile{
			ID:       idCounter,
			ParentID: parentID,
			Name:     d.Name(),
			FType:    ftype,
			Size:     fileInfo.Size(),
			CTime:    fileInfo.ModTime(),
		}

		// items = append(items, item)

		_, err = storage.CreateFile(item)
		if err != nil {
			return err
		}

		// Если это папка, запоминаем её ID для будущих детей
		if d.IsDir() {
			pathToID[path] = idCounter
		}

		// // Проверяем, что это: папка или файл
		// if d.IsDir() {
		// 	fmt.Printf("[Папка] %s\n", path)
		// } else {
		// 	fmt.Printf("[Файл ] %s\n", path)
		// }

		// NOTE: как получить информацию
		// fmt.Println(d.Info())

		idCounter++
		return nil // nil означает "продолжить обход"
	})

	if err != nil {
		return err
	}

	return nil
}
