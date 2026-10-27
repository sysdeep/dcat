#pragma once
#include "./main_window_geometry.hpp"
#include <GLFW/glfw3.h>

namespace UI
{
    class ImGuiFactory
    {
    public:
        ImGuiFactory(MainWindowGeometry geo);

        GLFWwindow *init(const char *title);
        void shutdown(GLFWwindow *window);

    private:
        MainWindowGeometry _geo;
    };
}