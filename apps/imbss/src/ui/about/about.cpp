#include "about.hpp"
#include "imgui.h"
#include "version.hpp"

using namespace UI;
About::About(/* args */) : _is_open(false)
{
}

About::~About()
{
}

void About::draw()
{

    ImGuiWindowFlags window_flags = ImGuiWindowFlags_NoResize |
                                    ImGuiWindowFlags_NoSavedSettings |
                                    ImGuiWindowFlags_NoCollapse;
    ImGui::SetNextWindowSize(ImVec2(300.f, 200.f));
    if (_is_open)
    {
        ImGui::Begin("About", &_is_open, window_flags);
        ImGui::Text("Простой календарик");
        ImGui::Dummy(ImVec2(0.0f, 16.0f));
        ImGui::Text("Version  : %s", PROJECT_VERSION);
        ImGui::Text("Author   : sysdeep@yandex.ru");
        // ImGui::Text("Repo     : TODO");
        ImGui::End();
    }
}

void About::show()
{
    _is_open = true;
}