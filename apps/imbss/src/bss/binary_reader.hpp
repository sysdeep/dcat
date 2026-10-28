#pragma once

#include <iostream>
#include <vector>
#include <cstdint>
#include <cstring>

// ==========================================
// КЛАСС ДЛЯ ЧТЕНИЯ (ДЕСЕРИАЛИЗАЦИЯ)
// ==========================================
class BinaryReader
{
private:
    const std::vector<uint8_t> &buffer;
    size_t offset = 0;

public:
    BinaryReader(const std::vector<uint8_t> &buf) : buffer(buf) {}

    // Чтение целых чисел из Little-Endian
    template <typename T>
    T read_int()
    {
        size_t bytes = sizeof(T);
        if (offset + bytes > buffer.size())
        {
            throw std::runtime_error("Данные закончились (Buffer underflow)");
        }

        T value = 0;
        for (size_t i = 0; i < bytes; ++i)
        {
            // Собираем число обратно, сдвигая байты влево
            value |= static_cast<T>(buffer[offset + i]) << (i * 8);
        }
        offset += bytes;
        return value;
    }

    // Чтение чисел с плавающей точкой
    template <typename T>
    T read_float()
    {
        typename std::conditional<sizeof(T) == 4, uint32_t, uint64_t>::type temp = read_int<decltype(temp)>();
        T value;
        std::memcpy(&value, &temp, sizeof(T));
        return value;
    }

    // Добавить внутрь класса BinaryReader:
    std::string read_string()
    {
        // 1. Читаем длину строки
        uint16_t length = read_int<uint16_t>();

        // Безопасность: проверяем, хватает ли данных в буфере
        if (offset + length > buffer.size())
        {
            throw std::runtime_error("Строка повреждена или буфер слишком мал");
        }

        // 2. Создаем строку напрямую из участка памяти вектора
        std::string str(reinterpret_cast<const char *>(&buffer[offset]), length);
        offset += length;

        return str;
    }

    // ==========================================
    // Добавить внутрь класса BinaryReader:
    // ==========================================

    // Универсальный метод чтения вектора
    template <typename T>
    std::vector<T> read_vector()
    {
        uint32_t size = read_int<uint32_t>();
        std::vector<T> vec;
        vec.reserve(size); // Выделяем память заранее для скорости

        for (uint32_t i = 0; i < size; ++i)
        {
            if constexpr (std::is_same_v<T, std::string>)
            {
                vec.push_back(read_string());
            }
            else if constexpr (std::is_floating_point_v<T>)
            {
                vec.push_back(read_float<T>());
            }
            else if constexpr (std::is_integral_v<T>)
            {
                vec.push_back(read_int<T>());
            }
            else
            {
                // Для пользовательских структур
                T item;
                item.deserialize(*this);
                vec.push_back(item);
            }
        }
        return vec;
    }

    // Быстрый метод чтения вектора (ТОЛЬКО для простых типов)
    template <typename T>
    std::vector<T> read_raw_vector()
    {
        static_assert(std::is_trivial_v<T>, "Этот метод только для простых типов данных!");

        uint32_t size = read_int<uint32_t>();
        size_t bytes_to_read = size * sizeof(T);

        if (offset + bytes_to_read > buffer.size())
        {
            throw std::runtime_error("Вектор поврежден или буфер слишком мал");
        }

        std::vector<T> vec(size);
        if (size > 0)
        {
            std::memcpy(vec.data(), &buffer[offset], bytes_to_read);
            offset += bytes_to_read;
        }
        return vec;
    }
};