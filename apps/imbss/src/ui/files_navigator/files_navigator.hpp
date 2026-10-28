#pragma once
#include "imgui.h"
#include "app/volume_provider.hpp"
#include "app/volume_state.hpp"

namespace UI
{

    class FilesNavigator
    {
    public:
        FilesNavigator(APP::VolumeProvider *volume_provider);
        ~FilesNavigator();
        void draw();

    private:
        // data
        ImGuiWindowFlags _window_flags;
        APP::VolumeProvider *_volume_provider;
        APP::VolumeState *_volume_state;

        void
        _draw_table();

        bool _open_volume();
        std::vector<domain::FileRecord> _get_files();
    };
}