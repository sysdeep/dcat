#pragma once
#include "calendar_model.hpp"

namespace UI
{
    class Selector
    {
    public:
        Selector(CalendarModel *model);
        void draw();

    private:
        CalendarModel *model;
    };
}