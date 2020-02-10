# 2019.12.26

бинарный формат с индексированием записей, создание и чтение - из файла

структура дерева хранится в индексе для быстрой итерации по дереву. Каждый индекс содержит id запаиси, ссылку на родителя, абсолютный адрес файловой записи в файле и длину данных

сами записи хранятся непрерывным списком структур

запись происходит непосредственно в файл при операции добавления, весь список данных не хранится в памяти. Отсюда - сначала записиываем данные, попутно формируем индекс, обновляем заголовок и записываем индекс

```
----------------------------
header
----------------------------
data
----------------------------
index dict
----------------------------
```

## Запись

- открываем файл
- смещаемся на длину заголовка
- сканируем папку и записываем данные файлов(формируем массив индексов в памяти)
- формируем бинарные данные в памяти
- записываем бинарные данные индексов после секции с данными файлов
- перемещаемся вначало
- формируем заголовок
- записываем заголовок

## Чтение

- открываем файл
- читаем и парсим заголовок
- узнаём о расположении секций
- читаем и парсим список индексов
- далее по запросу ищем в дереве индексов адреса данных файлов и последовательно их читаем из файла


## Плюсы

+ можно обработать много файлов(на тестах до 900000)
+ небольшое потребление памяти



## Минусы

- приходится загружать весь список индексов
- реализация поиска по имени - пока не понятно как...
- нельзя использовать сжатие на лету(в конце формируется заголовок, который записывается вначало файла)
- нельзя перезаписать файл, т.к. от открыт для чтения


## Дальнейшие мысли

- Можно загружать файл полностью в память - но при больших данных - это проблематично. Решаются проблемы с обновлением. Удаляется индекс.
- Можно использовать заголовок статистики, записанный в самом конце, и чтение производить с конца(как zip). Решается проблема сжатия на лету

## тек. реализация 2019.12.26
<!-- 
при создании базы из 74000 файлов, сканирование происходит быстро, но потом долго выполняются какие-то операции и подъедается память

при чтении такой базы - рутовые файлы выбираются шустро -->



## Тесты

Запись

^ кол-во файлов ^ размер базы 	^ время создания 	^ сжатый gzip вручную 	^ Путь 					^ SQL size	^
| 896833 		| 62.5 Mb 		| 25.5 с			| ---	 				| Development/_Comcon	| 			|
| 31105 		| 2.1 Mb 		| 0.8 с				| ---	 				| Android				| 9.7 Mb 	|
| 130	 		| 5.7 Kb 		| 0.017 с			| ---	 				| Music					|			|


Чтение

^ кол-во файлов ^ размер базы 	^ время создания 	^ сжатый gzip вручную 	^ Путь 					^ SQL size	^
| 896833 		| 62.5 Mb 		| 2.8 с				| ---	 				| Development/_Comcon	| 			|