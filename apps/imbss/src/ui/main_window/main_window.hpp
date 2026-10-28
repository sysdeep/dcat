#pragma once

#include <GLFW/glfw3.h>

#include "imgui.h"
#include "imgui_factory.hpp"
#include "./main_window_geometry.hpp"
#include "ui/files_navigator/files_navigator.hpp"

namespace UI
{

    class MainWindow
    {
    public:
        MainWindow(MainWindowGeometry geo);
        void loop();

    private:
        ImGuiFactory *factory;

        void _setup_configuration();
        void _setup_fonts();
        void _setup_style();

        void draw();

        // components
        FilesNavigator *_navigator;
    };

} // namespace UI
