#pragma once
#include "ui/main_window/main_window.hpp"
#include "ui/main_window/main_window_geometry.hpp"

class Application
{
public:
    Application(UI::MainWindowGeometry geo);
    void run();

private:
    UI::MainWindow *_main_window;
};
