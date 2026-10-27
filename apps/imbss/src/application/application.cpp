#include "./application.hpp"
#include <iostream>

Application::Application(UI::MainWindowGeometry geo)
{

    _main_window = new UI::MainWindow(geo);
}

void Application::run()
{

    _main_window->loop();
}
