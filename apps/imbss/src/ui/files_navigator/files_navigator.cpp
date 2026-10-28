#include "files_navigator.hpp"
#include "imgui.h"
#include <iostream>
#include <fstream>
#include <cstdint>
#include "bss/bss.hpp"
#include "bss/gzip_reader.hpp"
#include "ui/icons/icons.hpp"

using namespace UI;

FilesNavigator::FilesNavigator()
{
    _window_flags = ImGuiWindowFlags_NoDecoration |
                    ImGuiWindowFlags_NoMove |
                    ImGuiWindowFlags_NoResize |
                    ImGuiWindowFlags_NoSavedSettings |
                    ImGuiWindowFlags_NoBringToFrontOnFocus;
}

void FilesNavigator::draw()
{

    // geometry
    ImGuiViewport *viewport = ImGui::GetMainViewport();
    float width = viewport->WorkSize.x;
    float height = viewport->WorkSize.y;
    float start_x = viewport->WorkPos.x;
    float start_y = viewport->WorkPos.y;
    ImGui::SetNextWindowPos(ImVec2(start_x, start_y));
    ImGui::SetNextWindowSize(ImVec2(width, height));

    ImGui::Begin("Navigator", nullptr, _window_flags);
    ImGui::Text("Hello!!!!");
    if (ImGui::Button("start"))
    {

        _open_volume();
    }

    // file header
    ImGui::Text("File magic:   %d", _volume.header.magic);
    ImGui::Text("File version: %d", _volume.header.version);
    ImGui::Dummy(ImVec2(0.f, 16.f));

    ImGui::Text("Volume created:      %ld", _volume.description.created);
    ImGui::Text("Volume icon:         %d", _volume.description.icon);
    ImGui::Text("Volume records:      %ld", _volume.description.records);
    ImGui::Text("Volume name:         %s", _volume.description.name.c_str());
    ImGui::Text("Volume scan_path:    %s", _volume.description.scan_path.c_str());
    ImGui::Text("Volume description:  %s", _volume.description.description.c_str());
    ImGui::Dummy(ImVec2(0.f, 16.f));

    ImGui::Text("Records count:  %ld", _volume.records.size());
    ImGui::Dummy(ImVec2(0.f, 16.f));

    _draw_table();
    ImGui::End();
}

void FilesNavigator::_draw_table()
{
    if (ImGui::BeginTable("files_list", 3))
    {

        // header
        ImGui::TableNextRow();
        int index = 0;
        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "file");

        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "size");

        ImGui::TableSetColumnIndex(index++);
        ImGui::Text("%s", "date");

        // body
        for (FileRecord fr : _volume.records)
        {

            // icon
            std::string_view currentIcon = Icons::Search;
            if (fr.ftype == 1)
            {
                currentIcon = Icons::Folder;
            }
            else if (fr.ftype == 2)
            {
                currentIcon = Icons::File;
            }

            ImGui::TableNextRow();

            int column = 0;
            ImGui::TableSetColumnIndex(column++);
            ImGui::Text("%s %s", currentIcon.data(), fr.name.c_str());

            ImGui::TableSetColumnIndex(column++);
            ImGui::Text("%ld", fr.size);

            ImGui::TableSetColumnIndex(column++);
            ImGui::Text("%ld", fr.time);
        }
        ImGui::EndTable();
    }
}

bool FilesNavigator::_open_volume()
{

    const std::string filePath = "/tmp/example-db";
    std::cout << "start open volume" << std::endl;
    std::vector<uint8_t> buffer;

    if (readGzipToBuffer(filePath, buffer))
    {
        _volume = unmarshal(buffer);

        std::cout << "Volume header version: " << _volume.header.version << std::endl;
        std::cout << "Volume header magic: " << _volume.header.magic << std::endl;

        std::cout << "Volume created: " << _volume.description.created << std::endl;
        std::cout << "Volume icon: " << _volume.description.icon << std::endl;
        std::cout << "Volume records: " << _volume.description.records << std::endl;
        std::cout << "Volume name: " << _volume.description.name << std::endl;
        std::cout << "Volume scan_path: " << _volume.description.scan_path << std::endl;
        std::cout << "Volume description: " << _volume.description.description << std::endl;
    }
    else
    {
        std::cerr << "Unable read " << std::endl;
    }

    return true;
}