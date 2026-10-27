#include "calendar_model.hpp"
#include <algorithm>
#include <iostream>

using namespace UI;
CalendarModel::CalendarModel()
{

    time_t now = time(nullptr);
    auto ltm = localtime(&now);

    this->current_year = 1900 + ltm->tm_year;
    this->current_month = 1 + ltm->tm_mon;
    this->current_day = ltm->tm_mday;

    this->prepare(current_year, current_month);
}

void CalendarModel::go_next_month()
{
    auto new_month = this->month + 1;
    auto new_year = this->year;
    if (new_month > 12)
    {
        new_month = 1;
        new_year++;
    }

    this->go_to(new_year, new_month);
}

void CalendarModel::go_prev_month()
{
    auto new_month = this->month - 1;
    auto new_year = this->year;
    if (new_month < 1)
    {
        new_month = 12;
        new_year--;
    }

    this->go_to(new_year, new_month);
}

void CalendarModel::go_next_year()
{
    this->go_to(this->year + 1, this->month);
}

void CalendarModel::go_prev_year()
{
    this->go_to(this->year - 1, this->month);
}

void CalendarModel::go_now()
{
    time_t now = time(nullptr);
    auto ltm = localtime(&now);

    this->go_to(1900 + ltm->tm_year, 1 + ltm->tm_mon);
}

void CalendarModel::go_to(int year, int month)
{

    this->prepare(year, month);
}

void CalendarModel::prepare(int year, int month)
{
    this->year = year;
    this->month = month;

    auto days_in_month = calendar::days_in_month(this->year, this->month);

    // build days
    this->days.clear();
    for (int day = 0; day < days_in_month; day++)
    {
        auto wd = calendar::day_of_week(day + 1, month, year);
        this->days.push_back(Day{day + 1, wd});
    }

    // OK
    // for (const auto &d : this->days)
    // {
    //   std::cout << "Day: " << d.day << ", Weekday: " << static_cast<int>(d.weekday) << std::endl;
    // }

    /*
    Day: 1, Weekday: 0
  Day: 2, Weekday: 1
  Day: 3, Weekday: 2
  Day: 4, Weekday: 3
  Day: 5, Weekday: 4
  Day: 6, Weekday: 5
  Day: 7, Weekday: 6
  Day: 8, Weekday: 0
  Day: 9, Weekday: 1
  Day: 10, Weekday: 2
  Day: 11, Weekday: 3
  Day: 12, Weekday: 4
  Day: 13, Weekday: 5
  Day: 14, Weekday: 6
  Day: 15, Weekday: 0
  Day: 16, Weekday: 1
  Day: 17, Weekday: 2
  Day: 18, Weekday: 3
  Day: 19, Weekday: 4
  Day: 20, Weekday: 5
  Day: 21, Weekday: 6
  Day: 22, Weekday: 0
  Day: 23, Weekday: 1
  Day: 24, Weekday: 2
  Day: 25, Weekday: 3
  Day: 26, Weekday: 4
  Day: 27, Weekday: 5
  Day: 28, Weekday: 6
  Day: 29, Weekday: 0
  Day: 30, Weekday: 1
  Day: 31, Weekday: 2
    */
}

void CalendarModel::print()
{
    for (auto day : days)
    {
        std::cout << " " << day.day << "(" << get_weekday_name_short(day.weekday) << ")";
    }
    std::cout << std::endl;
}