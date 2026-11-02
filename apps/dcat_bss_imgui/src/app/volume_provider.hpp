#pragma once
#include <vector>
#include <string>
#include "domain/volume.hpp"

namespace APP
{
    class VolumeProvider
    {
    public:
        VolumeProvider();
        ~VolumeProvider();

        bool open(std::string filePath);
        bool is_opened{false};

        domain::Volume &get_volume();

    private:
        domain::Volume _volume;
    };
}