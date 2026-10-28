#pragma once

#include <iostream>
#include <vector>
#include <cstdint>
#include <cstring>

namespace bss
{

    // ==========================================
    // КЛАСС ДЛЯ ЗАПИСИ (СЕРИАЛИЗАЦИЯ)
    // ==========================================
    class BinaryWriter
    {
    public:
        std::vector<uint8_t> buffer;

        // Запись целых чисел любой разрядности в Little-Endian
        template <typename T>
        void write_int(T value)
        {
            size_t bytes = sizeof(T);
            for (size_t i = 0; i < bytes; ++i)
            {
                // Сдвигаем число вправо на 0, 8, 16, 24... бит и берем младший байт
                buffer.push_back(static_cast<uint8_t>((value >> (i * 8)) & 0xFF));
            }
        }

        // Запись чисел с плавающей точкой (float/double)
        template <typename T>
        void write_float(T value)
        {
            // Переинтерпретируем память float/double как целочисленный тип того же размера
            typename std::conditional<sizeof(T) == 4, uint32_t, uint64_t>::type temp;
            std::memcpy(&temp, &value, sizeof(T));
            write_int(temp);
        }

        // Добавить внутрь класса BinaryWriter:
        void write_string(const std::string &str)
        {
            // 1. Записываем длину строки как uint16_t в Little-Endian
            uint16_t length = static_cast<uint16_t>(str.size());
            write_int(length);

            // 2. Копируем сами символы строки в буфер
            if (length > 0)
            {
                buffer.insert(buffer.end(), str.begin(), str.end());
            }
        }

        // Универсальный метод (для векторов из ЛЮБЫХ типов, включая структуры и строки)
        template <typename T>
        void write_vector(const std::vector<T> &vec)
        {
            uint32_t size = static_cast<uint32_t>(vec.size());
            write_int(size); // Записываем количество элементов

            for (const auto &item : vec)
            {
                // Если это базовый тип (int, float), вызовется write_int/write_float.
                // Если у вас структура, можно перегрузить функцию или вызвать item.serialize(*this)
                if constexpr (std::is_same_v<T, std::string>)
                {
                    write_string(item);
                }
                else if constexpr (std::is_floating_point_v<T>)
                {
                    write_float(item);
                }
                else if constexpr (std::is_integral_v<T>)
                {
                    write_int(item);
                }
                else
                {
                    // Для пользовательских структур, у которых есть метод serialize
                    item.serialize(*this);
                }
            }
        }

        // Быстрый метод оптимизации (ТОЛЬКО для простых типов: int32_t, float, char и т.д.)
        template <typename T>
        void write_raw_vector(const std::vector<T> &vec)
        {
            static_assert(std::is_trivial_v<T>, "Этот метод только для простых типов данных!");

            uint32_t size = static_cast<uint32_t>(vec.size());
            write_int(size);

            if (size > 0)
            {
                size_t bytes_to_copy = vec.size() * sizeof(T);
                size_t current_size = buffer.size();

                // Расширяем буфер под новые байты
                buffer.resize(current_size + bytes_to_copy);
                // Копируем всю память массива за один раз
                std::memcpy(&buffer[current_size], vec.data(), bytes_to_copy);
            }
        }
    };

    // int buffToInteger(char *buffer, int offset = 0)
    // {
    //     // int a = static_cast<int>(static_cast<unsigned char>(buffer[0]) << 24 |
    //     //     static_cast<unsigned char>(buffer[1]) << 16 |
    //     //     static_cast<unsigned char>(buffer[2]) << 8 |
    //     //     static_cast<unsigned char>(buffer[3]));

    //     // int a = int((unsigned char)(buffer[0]) << 24 |
    //     //         (unsigned char)(buffer[1]) << 16 |
    //     //         (unsigned char)(buffer[2]) << 8 |
    //     //         (unsigned char)(buffer[3]));

    //     int a = int((unsigned char)(buffer[0 + offset]) |
    //                 (unsigned char)(buffer[1 + offset]) << 8 |
    //                 (unsigned char)(buffer[2 + offset]) << 16 |
    //                 (unsigned char)(buffer[3 + offset]) << 24);

    //     return a;
    // }

}