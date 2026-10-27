#include <string>
#include <ctime>
#include "imgui.h"
#include "today_bar.hpp"
#include "ui/utils/utils.hpp"

using namespace UI;
TodayBar::TodayBar() {}

void TodayBar::draw()
{

    time_t now = time(nullptr);
    auto ltm = localtime(&now);

    auto current_year = 1900 + ltm->tm_year;
    auto current_month = 1 + ltm->tm_mon;
    auto current_day = ltm->tm_mday;

    auto current_month_str = TodayBar::fillNumber(current_month);
    auto current_day_str = TodayBar::fillNumber(current_day);

    auto current_hour_str = TodayBar::fillNumber(ltm->tm_hour);
    auto current_minute_str = TodayBar::fillNumber(ltm->tm_min);
    auto current_second_str = TodayBar::fillNumber(ltm->tm_sec);

    std::string now_date = (std::to_string(current_year) +
                            "-" + current_month_str +
                            "-" + current_day_str +
                            " " + current_hour_str + ":" + current_minute_str + ":" + current_second_str);

    auto Style = ImGui::GetStyle();
    ImGui::PushFont(nullptr, Style.FontSizeBase * 1.6f);

    if (ImGui::BeginTable("today_info", 1))
    {

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        CenterTextInCell(now_date.c_str());
        ImGui::EndTable(); // calendar_grid
    }
    ImGui::PopFont();

    // ImGui::Text("Today:");
    // ImGui::Text("Year: %d", model->year);
    // ImGui::Text("Month: %d", model->month);
    // ImGui::Text("Day: %d", model->current_day);
}

const std::string TodayBar::fillNumber(int number)
{
    if (number < 10)
    {
        return "0" + std::to_string(number);
    }
    else
    {
        return std::to_string(number);
    }
}