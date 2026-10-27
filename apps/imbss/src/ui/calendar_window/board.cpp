#include "board.hpp"
#include "imgui.h"
#include "src/calendar/core.hpp"
#include "ui/utils/utils.hpp"
#include <cmath>

using namespace UI;
Board::Board()
{

    // prepare data_model
    for (int c = 0; c < 7; c++)
    {
        for (int r = 0; r < 6; r++)
        {
            this->data_model.push_back(Day{0, calendar::Weekday::Sunday}); // empty cell
        }
    }
}

void Board::draw(CalendarModel *model)
{

    // cache
    if (this->last_month != model->month || this->last_year != model->year)
    {
        // fill board model
        _clear_data_model();
        _fill_data_model(model);

        this->last_month = model->month;
        this->last_year = model->year;
    }

    // draw table
    if (ImGui::BeginTable("calendar_grid", 7))
    {

        // week days header
        ImGui::TableNextRow();
        int index = 0;
        for (auto day : calendar::weekdays)
        {
            auto label = calendar::get_weekday_name_short(day);
            ImGui::TableSetColumnIndex(index++);
            // ImGui::Text("%s", label);
            CenterTextInCell(label);
        }

        // body
        // const int rows = std::ceil(double(this->data_model.size()) / 7.f);

        for (int row = 0; row < 6; row++)
        {

            ImGui::TableNextRow();

            for (int column = 0; column < 7; column++)
            {

                ImGui::TableSetColumnIndex(column);

                auto index = (row * 7) + column;
                auto day = this->data_model[index]; // день
                // std::cout
                //     << "----> day: " << day.day
                //     << "index: " << index
                //     << std::endl;

                // день недели не из тек. месяца - пустая ячейка
                if (day.day == 0)
                {
                    // подгоняем размер, чтобы пустая строка не схлопывалась
                    ImVec2 rect = ImGui::GetItemRectSize();
                    ImGui::Dummy(rect);

                    continue;
                }

                bool is_current_day = day_is_current(day, model);
                if (is_current_day)
                {
                    ImGui::PushStyleColor(ImGuiCol_Button, (ImVec4)ImColor::HSV(5 / 7.0f, 0.6f, 0.6f));
                    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, (ImVec4)ImColor::HSV(5 / 7.0f, 0.7f, 0.7f));
                    ImGui::PushStyleColor(ImGuiCol_ButtonActive, (ImVec4)ImColor::HSV(5 / 7.0f, 0.8f, 0.8f));
                }

                bool is_weekend = day.weekday == calendar::Weekday::Sunday || day.weekday == calendar::Weekday::Saturday;
                if (is_weekend)
                {
                    ImGui::PushStyleColor(ImGuiCol_Button, (ImVec4)ImColor::HSV(3 / 7.0f, 0.6f, 0.6f));
                    ImGui::PushStyleColor(ImGuiCol_ButtonHovered, (ImVec4)ImColor::HSV(3 / 7.0f, 0.7f, 0.7f));
                    ImGui::PushStyleColor(ImGuiCol_ButtonActive, (ImVec4)ImColor::HSV(3 / 7.0f, 0.8f, 0.8f));
                }

                auto btn_text_model = std::to_string(day.day);
                ImGui::Button(btn_text_model.c_str(), ImVec2(-FLT_MIN, 0.0f));

                if (is_weekend)
                {
                    ImGui::PopStyleColor(3);
                }

                if (is_current_day)
                {
                    ImGui::PopStyleColor(3);
                }

                // auto btn_text_model = std::to_string(column * row);
                // if (ImGui::Button(btn_text_model.c_str(), ImVec2(-FLT_MIN, 0.0f)))
                // {
                //   this->on_day_clicked(column * row);
                // }
            }
        }
        ImGui::EndTable();
    }
}

bool Board::day_is_current(Day day, CalendarModel *model)
{
    if (model->current_year != model->year)
        return false;

    if (model->current_month != model->month)
        return false;

    return model->current_day == day.day;
}

void Board::_clear_data_model()
{
    for (auto &day : data_model)
    {
        day.day = 0;
        day.weekday = calendar::Weekday::Sunday;
    }
}

void Board::_fill_data_model(CalendarModel *model)
{

    // std::cout << "board before:" << std::endl;
    // _print_data_model();

    // std::cout << "model before:" << std::endl;
    // model->print();

    int month_day_index = 0;
    int data_model_index = 0;
    for (int r = 0; r < 6; r++)
    {

        // надо найти куда его вставить на доске, перебираем дни недели
        for (int i = 0; i < 7; i++)
        {

            // если не достигли конца модели
            if (month_day_index < model->days.size())
            {

                // берём день из пула модели
                auto day = model->days[month_day_index];

                // если день недели совпал, значит день обработали, переходим к след. в модели
                if (day.weekday == calendar::weekdays[i])
                {
                    data_model[data_model_index].day = day.day;
                    data_model[data_model_index].weekday = day.weekday;
                    month_day_index++;
                }
            }

            // иначе просто смещаемся по доске
            data_model_index++;
        }
    }

    // std::cout << "board after:" << std::endl;
    // _print_data_model();
}

void Board::_print_data_model()
{
    int gi = 0;
    for (int r = 0; r < 6; r++)
    {
        for (int c = 0; c < 7; c++)
        {
            auto day = data_model[gi];
            std::cout << " " << day.day << " ";
            gi++;
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}