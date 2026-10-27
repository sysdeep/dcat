#include "calendar.hpp"

using namespace calendar;

int calendar::days_in_month(int year, int month)
{
    if (month < 1 || month > 12)
        throw std::out_of_range("Month must be in the range 1..12");

    // Февраль – отдельный случай, потому что количество дней зависит от года
    if (month == 2)
        return is_leap_year(year) ? 29 : 28;

    // Для остальных месяцев берём значение из готовой таблицы
    return days_in_common_month[month - 1];
}

// void calendar::validate_date(int day, int month, int year)
// {
//     if (year < 1) // любой положительный год разрешён
//         throw std::out_of_range("Year must be >= 1");
//     if (month < 1 || month > 12)
//         throw std::out_of_range("Month must be in the range 1..12");
//     if (day < 1 || day > 31)
//         throw std::out_of_range("Day must be in the range 1..31");

//     // Дни, которые реально могут быть в данном месяце
//     constexpr std::array<int, 12> days_in_month_common{
//         31, 28, 31, 30, 31, 30,
//         31, 31, 30, 31, 30, 31};

//     // Високосный год?
//     // constexpr auto is_leap = [](int y) constexpr noexcept
//     // {
//     //     return (y % 4 == 0) & amp;
//     //     &amp;
//     //     ((y % 100 != 0) || (y % 400 == 0));
//     // };

//     int max_day = days_in_month_common[month - 1];
//     if (month == 2 && is_leap_year(year))
//         ++max_day; // февраль в високосный год

//     if (day > max_day)
//         throw std::out_of_range("Invalid day for the given month/year");
// }

Weekday calendar::day_of_week(int day, int month, int year) noexcept
{
    // Перенос января и февраля в предыдущий год
    // (Zeller работает с «март‑февраль» как 3‑14)
    if (month <= 2)
    {
        month += 12;
        --year;
    }

    const int K = year % 100; // годы в столетии
    const int J = year / 100; // номер столетия

    // Формула Zeller'а для Григорианского календаря
    int h = (day + (13 * (month + 1)) / 5 + K + K / 4 + J / 4 + 5 * J) % 7;

    // h = 0 → Saturday, 1 → Sunday, … 6 → Friday
    // Нам удобнее иметь 0 = Sunday, поэтому делаем поправку:
    int w = (h + 6) % 7; // 0 = Sunday … 6 = Saturday

    return static_cast<Weekday>(w);
}

// Weekday day_of_week_checked(int day, int month, int year)
// {
//     validate_date(day, month, year);
//     return day_of_week(day, month, year);
// }

// std::array<std::string, 7> weekday_names{
//     "Sunday", "Monday", "Tuesday", "Wednesday",
//     "Thursday", "Friday", "Saturday"};

// std::string to_string(calendar::Weekday d) noexcept
// {
//     return weekday_names[static_cast<std::size_t>(d)];
// }