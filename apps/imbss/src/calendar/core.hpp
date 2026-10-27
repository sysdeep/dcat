#pragma once
#include <array>

namespace calendar
{

    // ---------------------------------------------------------------
    // 1. День недели как enum (удобно при работе в коде)
    // ---------------------------------------------------------------
    enum class Weekday : unsigned // 0 = Sunday, 1 = Monday, … 6 = Saturday
    {
        Sunday = 0,
        Monday,
        Tuesday,
        Wednesday,
        Thursday,
        Friday,
        Saturday
    };

    constexpr std::array<Weekday, 7> weekdays{
        Weekday::Monday,
        Weekday::Tuesday,
        Weekday::Wednesday,
        Weekday::Thursday,
        Weekday::Friday,
        Weekday::Saturday,
        Weekday::Sunday,
    };

    constexpr const char *const weekdays_short[] = {
        "Вс", // Sunday = 0
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб",
    };

    constexpr const char *const weekdays_long[] = {
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    };

    const char *get_weekday_name(Weekday weekday);
    const char *get_weekday_name_short(Weekday weekday);

    // month ------------------------------------------------------------------
    enum class Month : unsigned // 0 = Sunday, 1 = Monday, … 6 = Saturday
    {
        January = 0,
        February,
        March,
        April,
        May,
        June,
        July,
        August,
        September,
        October,
        November,
        December
    };

    constexpr const char *const month_names[] = {
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    };

    const char *get_month_name(Month month);
}