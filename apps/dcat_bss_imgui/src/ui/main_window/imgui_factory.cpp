#include "imgui_factory.hpp"
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <GLFW/glfw3.h>
#include <iostream>

using namespace UI;
ImGuiFactory::ImGuiFactory(MainWindowGeometry geo) : _geo(geo) {};
GLFWwindow *ImGuiFactory::init(const char *title)
{

    GLFWwindow *window = nullptr;

    // glfw
    glfwSetErrorCallback(
        [](int error, const char *description)
        { fprintf(stderr, "GLFW Error %d: %s\n", error, description); });

    if (!glfwInit())
    {
        // log::fatal("Failed to initialize GLFW!");
        std::abort();
    }

// TODO: glsl_version - see initImGui
// Decide GL+GLSL versions
#if defined(IMGUI_IMPL_OPENGL_ES2)
    // GL ES 2.0 + GLSL 100
    const char *glsl_version = "#version 100";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 2);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
    glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_ES_API);
#elif defined(__APPLE__)
    // GL 3.2 + GLSL 150
    const char *glsl_version = "#version 150";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // 3.2+ only
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);           // Required on Mac
#else
    // GL 3.0 + GLSL 130
    const char *glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
    // glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+
    // only glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // 3.0+ only
#endif

    // Set window hints for an undecorated window
    // glfwWindowHint(GLFW_DECORATED, GLFW_FALSE);

    // Create window with graphics context
    window = glfwCreateWindow(_geo.width, _geo.height, title, nullptr, nullptr);
    if (window == nullptr)
        std::abort();

    // move window
    if (_geo.padx != 0 || _geo.pady != 0)
    {

        if (window)
        {
            // 2. Получаем монитор, на котором запущено приложение (обычно это основной)
            GLFWmonitor *primary_monitor = glfwGetPrimaryMonitor();

            if (primary_monitor)
            {
                // 3. Получаем размеры РАБОЧЕЙ ОБЛАСТИ экрана (Workarea)
                // Это важно: функция учитывает размер панели задач Windows / дока macOS!
                int monitor_x, monitor_y, monitor_width, monitor_height;
                glfwGetMonitorWorkarea(primary_monitor, &monitor_x, &monitor_y, &monitor_width, &monitor_height);

                // если отступ отрицательный - отсчёт от правого края
                int target_x = 0;
                if (_geo.padx < 0)
                {
                    target_x = monitor_x + monitor_width - _geo.width;
                }

                // если отступ отрицательный - отсчёт от нижнего края
                int target_y = 0;
                if (_geo.pady < 0)
                {
                    target_y = monitor_y + monitor_height - _geo.height;
                }

                // padding
                target_x += _geo.padx;
                target_y += _geo.pady;

                // move
                glfwSetWindowPos(window, target_x, target_y);
            }
        }
    }

    glfwMakeContextCurrent(window);
    glfwSwapInterval(1); // Enable vsync

    // imgui ------------------------------------------------------------------
    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    auto io = &ImGui::GetIO();
    (void)io;
    io->ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard; // Enable Keyboard Controls
    // io->ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;  // Enable Gamepad Controls

    // Setup Platform/Renderer backends
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    return window;
};

void ImGuiFactory::shutdown(GLFWwindow *window)
{
    // destroy imgui
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    // destroy glfw
    glfwDestroyWindow(window);
    glfwTerminate();
};