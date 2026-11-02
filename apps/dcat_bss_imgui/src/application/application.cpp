#include "./application.hpp"
#include <iostream>

Application::Application(UI::MainWindowGeometry geo)
{
    _volume_provider = new APP::VolumeProvider();
    _main_window = new UI::MainWindow(geo, _volume_provider);
}

void Application::run()
{

    _main_window->loop();
}
