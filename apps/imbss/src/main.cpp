#include <ctime>
#include <iostream>

#include "application/application.hpp"
#include "argparse/argparse.hpp"
#include "ui/main_window/main_window_geometry.hpp"
#include "version.hpp"

int main(int argc, const char *const *argv)
{

    // argparse ---------------------------------------------------------------
    argparse::ArgumentParser program("imcalendar", PROJECT_VERSION);

    // program.add_argument("--padx")
    //     .help("x offset, positive - from left, negative - from right")
    //     .scan<'i', int>();

    // program.add_argument("--pady")
    //     .help("y offset, positive - from top, negative - from bottom")
    //     .scan<'i', int>();

    try
    {
        program.parse_args(argc, argv);
    }
    catch (const std::exception &err)
    {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(1);
    }

    UI::MainWindowGeometry mwGeo{
        800, // width
        600, // height
        0,   // padx
        0,   // pady
    };

    // if (program.is_used("--padx"))
    // {
    //     mwGeo.padx = program.get<int>("--padx");
    // }

    // if (program.is_used("--pady"))
    // {
    //     mwGeo.pady = program.get<int>("--pady");
    // }

    // application ------------------------------------------------------------
    auto app = new Application(mwGeo);
    app->run();

    return 0;
}
