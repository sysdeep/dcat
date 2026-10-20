package scanner

import (
	"dcat/internal/stor"
	"fmt"
	"io/fs"
	"path/filepath"
)

func Scan(root string) ([]stor.FileRecord, error) {

	root = filepath.Clean(root)

	var items []stor.FileRecord
	var idCounter uint64 = 1

	// Мапа для связи "Путь к папке -> Числовой ID папки"
	pathToID := make(map[string]uint64)

	// 1. Создаем и добавляем корень
	rootItem := stor.FileRecord{
		ID:       idCounter,
		ParentID: 0, // У корня нет родителя
		Name:     filepath.Base(root),
		Path:     root,
		IsDir:    true,
		Size:     0,
	}
	items = append(items, rootItem)
	pathToID[root] = idCounter
	idCounter++

	err := filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			// TODO
			// // Ошибка доступа к файлу/папке (например, нет прав)
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

		// Создаем плоский элемент
		item := stor.FileRecord{
			ID:       idCounter,
			ParentID: parentID,
			Name:     d.Name(),
			Path:     path,
			IsDir:    d.IsDir(),
			Size:     0, // TODO
		}

		items = append(items, item)

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
		fmt.Printf("Обход завершился с ошибкой: %v\n", err)
		return nil, err
	}

	return items, nil
}

// FLAT
/*

package main

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"path/filepath"
)

// FileItem представляет плоский элемент файловой системы
type FileItem struct {
	ID       int    `json:"id"`
	ParentID int    `json:"parent_id"` // 0 для корневого каталога
	Name     string `json:"name"`
	Path     string `json:"path"`
	IsDir    bool   `json:"is_dir"`
}

func BuildFlatFileList(rootDir string) ([]FileItem, error) {
	rootDir = filepath.Clean(rootDir)

	var items []FileItem
	idCounter := 1

	// Мапа для связи "Путь к папке -> Числовой ID папки"
	pathToID := make(map[string]int)

	// 1. Создаем и добавляем корень
	rootItem := FileItem{
		ID:       idCounter,
		ParentID: 0, // У корня нет родителя
		Name:     filepath.Base(rootDir),
		Path:     rootDir,
		IsDir:    true,
	}
	items = append(items, rootItem)
	pathToID[rootDir] = idCounter
	idCounter++

	// 2. Обходим каталог
	err := filepath.WalkDir(rootDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		// Пропускаем сам корень, мы его добавили вручную
		if path == rootDir {
			return nil
		}

		// Вычисляем путь родителя
		parentDir := filepath.Dir(path)
		parentID, exists := pathToID[parentDir]
		if !exists {
			return fmt.Errorf("родительский ID не найден для: %s", path)
		}

		// Создаем плоский элемент
		item := FileItem{
			ID:       idCounter,
			ParentID: parentID,
			Name:     d.Name(),
			Path:     path,
			IsDir:    d.IsDir(),
		}

		items = append(items, item)

		// Если это папка, запоминаем её ID для будущих детей
		if d.IsDir() {
			pathToID[path] = idCounter
		}

		idCounter++
		return nil
	})

	if err != nil {
		return nil, err
	}

	return items, nil
}


-------

func main() {
	targetDir := "./my_folder"

	flatList, err := BuildFlatFileList(targetDir)
	if err != nil {
		fmt.Printf("Ошибка: %v\n", err)
		return
	}

	// Выводим в формате JSON, чтобы увидеть плоскую структуру
	jsonData, _ := json.MarshalIndent(flatList, "", "  ")
	fmt.Println(string(jsonData))
}


*/

// TREE
/*
package main

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"path/filepath"
)

// Node представляет элемент файловой системы (файл или папку)
type Node struct {
	Name     string   `json:"name"`
	Path     string   `json:"path"`
	IsDir    bool     `json:"is_dir"`
	Children []*Node  `json:"children,omitempty"` // Будет nil для файлов, скрывается в JSON если пустой
}

func BuildFileTree(rootDir string) (*Node, error) {
	// Очищаем и абсолютизируем путь для корректного разбиения на папки
	rootDir = filepath.Clean(rootDir)

	// Корень нашего дерева
	rootNode := &Node{
		Name:  filepath.Base(rootDir),
		Path:  rootDir,
		IsDir: true,
	}

	// Мапа для быстрого поиска созданных папок по их путям
	nodesMap := make(map[string]*Node)
	nodesMap[rootDir] = rootNode

	// Обходим файловую систему
	err := filepath.WalkDir(rootDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		// Пропускаем сам корень, мы его уже создали
		if path == rootDir {
			return nil
		}

		// Создаем новый узел для текущего файла/папки
		newNode := &Node{
			Name:  d.Name(),
			Path:  path,
			IsDir: d.IsDir(),
		}

		// Находим родительскую директорию текущего элемента
		parentDir := filepath.Dir(path)
		parentNode, exists := nodesMap[parentDir]

		if exists {
			// Добавляем текущий элемент в список детей его родителя
			parentNode.Children = append(parentNode.Children, newNode)
		} else {
			// Это редкий случай, если по какой-то причине родитель не обошелся раньше
			// (в рамках WalkDir такого происходить не должно)
			return fmt.Errorf("родительский каталог не найден для пути: %s", path)
		}

		// Если текущий элемент — папка, запоминаем его в мапу, чтобы к нему могли привязаться его дети
		if d.IsDir() {
			nodesMap[path] = newNode
		}

		return nil
	})

	if err != nil {
		return nil, err
	}

	return rootNode, nil
}

*/
