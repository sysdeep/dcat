# 2019.12.26

бинарный формат с индексированием записей

структура дерева хранится в индексе для быстрой итерации по дереву. Каждый индекс содержит id запаиси, ссылку на родителя, относительный адрес файловой записи в списке и длину данных

сами записи хранятся непрерывным списком структур

```
----------------------------
header
----------------------------
index dict
----------------------------
data
----------------------------
```


## тек. реализация 2019.12.26

при создании базы из 74000 файлов, сканирование происходит быстро, но потом долго выполняются какие-то операции и подъедается память

при чтении такой базы - рутовые файлы выбираются шустро
