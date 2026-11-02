#include "gzip_reader.hpp"

namespace APP
{
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
}