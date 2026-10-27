#pragma once
#include "calendar/calendar.hpp"
#include "calendar_model.hpp"
#include <vector>

namespace UI
{
    class Board
    {
    public:
        Board();

        void draw(CalendarModel *model);

    private:
        // cache
        int last_year = -1;
        int last_month = -1;

        // сетка 7х5
        std::vector<Day> data_model;

        bool day_is_current(Day day, CalendarModel *model);

        void _clear_data_model();
        void _fill_data_model(CalendarModel *model);
        void _print_data_model();
    };
} // namespace UI
