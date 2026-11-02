# Multi Volume SQLite

Формат хранения на базе sqlite с несколькими томами.
Является основным форматом для оригинальной реализации dcat.

Описание томов и файлов хранятся в SQL-таблицах.

**Достоинства**

- модификация хранилища

**Недостатки**

- размер файла при большом кол-ве записей
- долгие операции при большом кол-ве записей

## Версии

тек. версия - **4**

### Миграции

#### 1 -> 2

```sql
INSERT INTO system(key, value) VALUES("updated",?)
ALTER TABLE volumes ADD COLUMN updated DATETIME
```

#### 2 -> 3

```sql
INSERT INTO system(key, value) VALUES("description",?)
ALTER TABLE volumes ADD COLUMN description TEXT
```

#### 3 -> 4

```sql
CREATE INDEX `uuid_index` ON `files` (`uuid` ASC);
CREATE INDEX `parent_id_index` ON `files` (`parent_id` ASC);
```

## Структура

### Таблица Volumes

Содержит описание тома

```sql
CREATE TABLE "volumes" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "uuid"      VARCHAR(64),
        "name"      VARCHAR(64),
        "path"      VARCHAR(256),
        "created"   DATETIME,
        "updated"   DATETIME,
        "vtype"         VARCHAR(32),
        "description"   TEXT
    );
```

```python
VOLUME_TYPE = ("cd", "audio_cd", "dvd", "folder",
	"hdd", "hdd_usb", "flash", "sd", "floppy", "net", "tape", "crypted", "bdrom"
			   # "other"
			   )
```

### Таблица Files

```sql
CREATE TABLE "files" (
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "volume_id"     INTEGER NOT NULL,
        "uuid"          VARCHAR(64),
        "parent_id"     VARCHAR(64),
        "name"          VARCHAR(64) NOT NULL,
        "type"          INTEGER NOT NULL,
        "rights"        INTEGER,
        "sowner"        VARCHAR(64),
        "sgroup"        VARCHAR(64),
        "ctime"         INTEGER,
        "atime"         INTEGER,
        "mtime"         INTEGER,
        "category"      INTEGER,
        "description"   TEXT,
        "size"          INTEGER

    );

CREATE INDEX `uuid_index` ON `files` (`uuid` ASC);
CREATE INDEX `parent_id_index` ON `files` (`parent_id` ASC);
```

- **type**
  - DIR = 0
  - FILE = 1

### Таблица System

По факту является key-value и хранит произвольные метаданные

```sql
CREATE TABLE "system" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "key"       VARCHAR(64),
        "value"     VARCHAR(64)
    );
```

```python
CREATE_VERSION = """
    INSERT INTO system(key, value) VALUES("version",?)
"""

CREATE_TIMESTAMP_CREATED = """
    INSERT INTO system(key, value) VALUES("created",?)
"""

CREATE_TIMESTAMP_UPDATED = """
    INSERT INTO system(key, value) VALUES("updated",?)
"""

CREATE_SYSTEM_DESCRIPTION = """
    INSERT INTO system(key, value) VALUES("description",?)
"""
```

- **version**
- **created**
- **updated**
- **description**
