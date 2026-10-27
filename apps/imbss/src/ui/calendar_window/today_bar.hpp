#pragma once
#include <string>

namespace UI
{
    class TodayBar
    {
    public:
        TodayBar();
        void draw();

        static const std::string fillNumber(int number);
    };
}