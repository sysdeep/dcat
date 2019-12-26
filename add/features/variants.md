# Варианты



## BinVolDict Бинарный формат с жатием и оглавлением

```
----------------------
header
----------------------
dict
----------------------
data
----------------------
```

в словаре содержаться структуры вида:

```
id
parent_id
data_addr
```

данные сжимаются gzip и хранятся как непрерывный поток байт. Адрес начала 1 структуры данных хранится в словаре


Преимущества:

- достаточно быстрый поиск в дереве - нужно только итерироваться по словарю, который имеет определённую структуру