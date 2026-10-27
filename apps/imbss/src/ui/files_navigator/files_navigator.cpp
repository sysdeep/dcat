#include "files_navigator.hpp"
#include "imgui.h"

using namespace UI;

FilesNavigator::FilesNavigator()
{
    _window_flags = ImGuiWindowFlags_NoDecoration |
                    ImGuiWindowFlags_NoMove |
                    ImGuiWindowFlags_NoResize |
                    ImGuiWindowFlags_NoSavedSettings |
                    ImGuiWindowFlags_NoBringToFrontOnFocus;
}

void FilesNavigator::draw()
{

    // geometry
    ImGuiViewport *viewport = ImGui::GetMainViewport();
    float width = viewport->WorkSize.x / 2;
    float height = viewport->WorkSize.y;
    float start_x = viewport->WorkPos.x;
    float start_y = viewport->WorkPos.y;
    ImGui::SetNextWindowPos(ImVec2(start_x, start_y));
    ImGui::SetNextWindowSize(ImVec2(width, height));

    ImGui::Begin("Navigator", nullptr, _window_flags);
    ImGui::Text("Hello!!!!");
    _draw_table();
    ImGui::End();
}

void FilesNavigator::_draw_table()
{
    if (ImGui::BeginTable("files_list", 3))
    {

        // header
        ImGui::TableNextRow();
        int index = 0;
        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "file");

        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "size");

        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "date");

        // body

        for (int row = 0; row < 66; row++)
        {

            ImGui::TableNextRow();

            for (int column = 0; column < 3; column++)
            {

                ImGui::TableSetColumnIndex(column);
                ImGui::Text("%s", "foo");
            }
        }
        ImGui::EndTable();
    }
}