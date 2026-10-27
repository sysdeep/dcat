#include "calendar_window.hpp"
#include "calendar/calendar.hpp"
#include "imgui.h"
#include "ui/utils/utils.hpp"
#include "version.hpp"
#include <ctime>
#include <iostream>
#include <ostream>
#include <string>

using namespace UI;
CalendarWindow::CalendarWindow()
{

    this->window_flags = ImGuiWindowFlags_NoDecoration |
                         ImGuiWindowFlags_NoMove |
                         ImGuiWindowFlags_NoResize |
                         ImGuiWindowFlags_NoSavedSettings |
                         ImGuiWindowFlags_NoBringToFrontOnFocus;

    // // current date/time based on current system
    this->model = new CalendarModel();
    this->board = new Board();
    this->selector = new Selector(this->model);
    this->today_bar = new TodayBar();

    this->is_about = true;
    this->about = new About();
}

void CalendarWindow::draw()
{

    ImGuiViewport *viewport = ImGui::GetMainViewport();
    auto size = ImVec2(viewport->WorkSize.x / 2, viewport->WorkSize.y);
    ImGui::SetNextWindowPos(ImVec2(viewport->WorkPos.x + viewport->WorkSize.x / 2, viewport->WorkPos.y));
    ImGui::SetNextWindowSize(size);

    ImGui::Begin("CalendarWindow", nullptr, window_flags);

    today_bar->draw();
    ImGui::Dummy(ImVec2(0.0f, 16.0f));
    selector->draw();
    ImGui::Dummy(ImVec2(0.0f, 16.0f));
    board->draw(this->model);

    ImGui::Dummy(ImVec2(0.0f, 16.0f));

    // info bar
    ImGui::Text("v %s", PROJECT_VERSION);
    if (ImGui::IsItemClicked())
    {
        this->about->show();
    }

    // about ----------------------------------------------
    this->about->draw();

    ImGui::End();
}
