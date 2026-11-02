#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <string>
#include <zlib.h> // Обязательно подключить zlib

// TODO: вынести отсюда и оформить

namespace APP
{

    bool readGzipToBuffer(const std::string &filename, std::vector<uint8_t> &buffer);

    // bool readSimpleFile(const std::string &filename, std::vector<int8_t> &buffer)
    // {
    //     std::ifstream file(filename, std::ios::binary | std::ios::ate);
    //     if (!file.is_open())
    //     {
    //         return false; // Не удалось открыть файл
    //     }

    //     std::streamsize fileSize = file.tellg();
    //     if (fileSize <= 0)
    //     {
    //         buffer.clear();
    //         return true; // Файл пустой
    //     }

    //     // 3. Возвращаем указатель в начало файла для чтения
    //     file.seekg(0, std::ios::beg);

    //     // 4. Выделяем память в векторе под размер файла
    //     buffer.resize(static_cast<std::size_t>(fileSize));

    //     // 5. Читаем данные напрямую в буфер вектора
    //     // Метод read ожидает char*, поэтому делаем reinterpret_cast
    //     if (!file.read(reinterpret_cast<char *>(buffer.data()), fileSize))
    //     {
    //         return false; // Ошибка при чтении данных
    //     }

    //     return true;
    // }

}