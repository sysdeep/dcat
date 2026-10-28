#pragma once
#include "imgui.h"
#include "bss/bss.hpp"

// #define ICON_FOLDER "\uf07b"
// #define ICON_FILE "\uea7b"

namespace UI
{

    // const char *file = "\uea7b";
    // const char *folder = "\uf07b";

    class FilesNavigator
    {
    public:
        FilesNavigator(/* args */);
        ~FilesNavigator();
        void draw();

    private:
        ImGuiWindowFlags _window_flags;
        void _draw_table();

        Volume _volume;

        bool _open_volume();
    };
}