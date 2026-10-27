#pragma once
#include <string>

#include "board.hpp"
#include "calendar/calendar.hpp"
#include "calendar_model.hpp"
#include "imgui.h"
#include "selector.hpp"
#include "today_bar.hpp"
#include "ui/about/about.hpp"

namespace UI
{
    class CalendarWindow
    {
    public:
        CalendarWindow();
        void draw();

    private:
        ImGuiWindowFlags window_flags;
        CalendarModel *model;

        Board *board;
        Selector *selector;
        TodayBar *today_bar;
        About *about;
        bool is_about;
    };
} // namespace UI