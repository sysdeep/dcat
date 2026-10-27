#pragma once
#include "imgui.h"

namespace UI
{

    class FilesNavigator
    {
    public:
        FilesNavigator(/* args */);
        ~FilesNavigator();
        void draw();

    private:
        ImGuiWindowFlags _window_flags;
        void _draw_table();
    };
}