#include "selector.hpp"
#include "imgui.h"
#include "ui/utils/utils.hpp"

using namespace UI;

Selector::Selector(CalendarModel *model) : model(model) {}

void Selector::draw()
{

    // draw month selector
    if (ImGui::BeginTable("range_selector", 7))
    {
        ImGui::TableNextRow();

        // month ------------------------------------------
        ImGui::TableSetColumnIndex(0);
        if (ImGui::Button("<", ImVec2(-FLT_MIN, 0.0f)))
        {
            model->go_prev_month();
        }

        ImGui::TableSetColumnIndex(1);

        auto month_name = calendar::get_month_name(static_cast<calendar::Month>(model->month - 1));
        CenterTextInCell(month_name);

        ImGui::TableSetColumnIndex(2);

        if (ImGui::Button(">", ImVec2(-FLT_MIN, 0.0f)))
        {
            model->go_next_month();
        }

        // today ------------------------------------------
        ImGui::TableSetColumnIndex(3);
        // auto Style = ImGui::GetStyle();
        // ImGui::PushFont(nullptr, Style.FontSizeBase * 1.6f);
        if (ImGui::Button("\uf017", ImVec2(-FLT_MIN, 0.0f)))
        {
            model->go_now();
        }
        if (ImGui::IsItemHovered())
        {
            ImGui::SetTooltip("Сегодня");
        }
        // ImGui::PopFont();

        // year -------------------------------------------
        ImGui::TableSetColumnIndex(4);
        if (ImGui::Button("<##2", ImVec2(-FLT_MIN, 0.0f)))
        {
            model->go_prev_year();
        }

        ImGui::TableSetColumnIndex(5);

        CenterTextInCell(std::to_string(model->year).c_str());

        ImGui::TableSetColumnIndex(6);

        if (ImGui::Button(">##2", ImVec2(-FLT_MIN, 0.0f)))
        {
            model->go_next_year();
        }

        ImGui::EndTable();
    }
}