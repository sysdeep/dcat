# DCath

Проект предназначен для сохранения структуры каталога или диска в локальной базе данных с последующим просмотром и навигацией.
Является представителем программ - каталогизаторов.

### Требования

- python 3.5
- tkinter
- sqlite3






## Lin test

```

#--- lin
python3 ./main.py /home/nia/Development/_Python/_DCat/Export10/Apps.bm.gz
python3 ./main.py /home/nia/Development/_Python/_DCat/Export10/Video.bm.gz



#--- win
python3 main.py E:\_Wrk\_Python\_DCat\Bin10Test\files\P50.hmap.gz

```


Apps
- size - 2.6M
- records - 313057
- parse table - 0.53
- parse texts - 0.23






## Win test

```
python main.py "e:\_Wrk\_Python\_DCat\Export10\P80(25G).bm.gz"
```

- size - 380K
- records - 33584
- parce data - 0.18