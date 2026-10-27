#pragma once
#include "calendar/calendar.hpp"
#include <vector>

namespace UI
{
    struct Day
    {
        int day;
        calendar::Weekday weekday;
    };

    class CalendarModel
    {
    public:
        CalendarModel();

        int current_day;
        int current_year;
        int current_month;

        int year;
        int month;
        // int days_in_month;

        // содержит дни выбранного месяца
        std::vector<Day> days;

        void go_next_month();
        void go_prev_month();
        void go_next_year();
        void go_prev_year();
        void go_now();

        void go_to(int year, int month);

        void print();

    private:
        void prepare(int year, int month);
    };

}