#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <string>
#include <zlib.h> // Обязательно подключить zlib

// TODO: вынести отсюда и оформить

bool readGzipToBuffer(const std::string &filename, std::vector<uint8_t> &buffer)
{
    // 1. Открываем gzip-файл для чтения в бинарном режиме
    gzFile file = gzopen(filename.c_str(), "rb");
    if (!file)
    {
        return false; // Не удалось открыть файл
    }

    buffer.clear();

    // 2. Буфер для чтения порциями (размер чанка можно менять, 128 КБ — оптимально)
    const std::size_t chunkSize = 131072;
    std::vector<int8_t> tempChunk(chunkSize);

    // 3. Читаем файл порциями, пока не дойдем до конца
    while (true)
    {
        int bytesRead = gzread(file, tempChunk.data(), static_cast<unsigned int>(chunkSize));

        if (bytesRead > 0)
        {
            // Дописываем прочитанный чанк в конец основного буфера
            buffer.insert(buffer.end(), tempChunk.begin(), tempChunk.begin() + bytesRead);
        }
        else if (bytesRead == 0)
        {
            // Успешно дочитали до конца файла
            break;
        }
        else
        {
            // Произошла ошибка чтения (bytesRead < 0)
            gzclose(file);
            return false;
        }
    }

    // 4. Закрываем файл
    gzclose(file);
    return true;
}

bool readSimpleFile(const std::string &filename, std::vector<int8_t> &buffer)
{
    std::ifstream file(filename, std::ios::binary | std::ios::ate);
    if (!file.is_open())
    {
        return false; // Не удалось открыть файл
    }

    std::streamsize fileSize = file.tellg();
    if (fileSize <= 0)
    {
        buffer.clear();
        return true; // Файл пустой
    }

    // 3. Возвращаем указатель в начало файла для чтения
    file.seekg(0, std::ios::beg);

    // 4. Выделяем память в векторе под размер файла
    buffer.resize(static_cast<std::size_t>(fileSize));

    // 5. Читаем данные напрямую в буфер вектора
    // Метод read ожидает char*, поэтому делаем reinterpret_cast
    if (!file.read(reinterpret_cast<char *>(buffer.data()), fileSize))
    {
        return false; // Ошибка при чтении данных
    }

    return true;
}