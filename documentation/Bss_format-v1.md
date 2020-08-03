# Bss

Описание формата Bss - v1

Данные хранятся в сжатом(gzip) файле в бинарном виде.


## Форматы данных

- uint 4 - unsigned int 4 bytes (<I)(2 147 483 647)
- ushort 2 - unsigned short 2 bytes (<H)(65 535)
- ulong 8 - unsigned long long 8 bytes (<Q)(18 446 744 073 709 551 615)
- bstr - счётная строка [[str_len - ushort][binary string - str_len]]




## Структура документа

Данные располагаются последовательно в определённых секциях.

[magic][version][header_len][header_struct][magic][row_len][row_struct]...[row_len][row_struct][magic]

- magic 		[ushort 2] - идентификатор файла и метка контроля структуры
- version 		[ushort 2] - версия структуры файла
- header_len 	[ushort 2] - длина данных структуры заголовка
- row_len		[ushort 2] - длина данных структуры строки данных файла
- header_struct - структура заголовка
- row_struct - структура строки данных

Чтение из файла производится последовательно, начиная с начала.

По возможности записать кол-во файлов в заголовок






### magic

идентификатор файла - заданная константа для проверки типа файла

0xfafb(64251)




### Заголовок - header_struct

Содержит данные, описывающие свойства всего тома

[created][icon][records][name][scan_path][description]

- created 		[ulong 8]	- дата создания(unix timestamp)
- icon 			[ushort 2]	- id иконки
- records  		[ulong 8] 	- кол-во записей
- name 			[bstr]		- название тома
- scan_path		[bstr]		- путь до ресурса сканирования
- description 	[bstr]		- произвольное описание











## Структура Записи данных - row_struct

[type][size][ctime][rights][fid][pid][name][description]

- type 			[ushort 2]	- тип файла(каталог/файл...)
- size 			[ulong 8]	- размер файла
- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
- rights 		[ushort 2]	- код доступа(unix 777)
- fid 			[uint 4]	- id записи
- pid 			[uint 4]	- id родителя(0 - корень)
- name 			[bstr]		- название
- description 	[bstr]		- произвольное описание


Эти не пригодились ещё нигде...

- reserv 		[uint 4]	- резерв
- owner 		?[uint 4]	- владелец
- group			?[uint 4]	- группа






## Порядок чтения

- Открыть файл на чтение
- Проверить идентификатор
- Прочитать версию формата, и выбрать способ дальнейшего декодирования
- Прочитать размер заголовка
- Прочитать заголовок
- Проверить контроль
- Прочитать длину строки данных
- Прочитать строку данных
- Повторить чтение данных
- Проверить контроль

