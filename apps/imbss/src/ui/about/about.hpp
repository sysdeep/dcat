
#pragma once

namespace UI
{

    class About
    {
    private:
        bool _is_open;

    public:
        About(/* args */);
        ~About();
        void draw();
        void show();
    };

}