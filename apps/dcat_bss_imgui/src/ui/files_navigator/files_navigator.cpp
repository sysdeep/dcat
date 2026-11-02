#include "files_navigator.hpp"
#include "imgui.h"
#include <iostream>
#include <fstream>
#include <cstdint>
#include "app/bss/bss.hpp"
#include "app/gzip_reader.hpp"
#include "ui/icons/icons.hpp"

using namespace UI;

FilesNavigator::FilesNavigator(APP::VolumeProvider *volume_provider) : _volume_provider(volume_provider)
{
    _window_flags = ImGuiWindowFlags_NoDecoration |
                    ImGuiWindowFlags_NoMove |
                    ImGuiWindowFlags_NoResize |
                    ImGuiWindowFlags_NoSavedSettings |
                    ImGuiWindowFlags_NoBringToFrontOnFocus;

    _volume_state = new APP::VolumeState(volume_provider);
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

    auto _volume = _volume_provider->get_volume();
    // file header
    ImGui::Text("File magic:   %d", _volume.meta.magic);
    ImGui::Text("File version: %d", _volume.meta.version);
    ImGui::Dummy(ImVec2(0.f, 16.f));

    ImGui::Text("Volume created:      %ld", _volume.description.created);
    ImGui::Text("Volume icon:         %d", _volume.description.icon);
    ImGui::Text("Volume records:      %ld", _volume.description.records);
    ImGui::Text("Volume name:         %s", _volume.description.name.c_str());
    ImGui::Text("Volume scan_path:    %s", _volume.description.scan_path.c_str());
    ImGui::Text("Volume description:  %s", _volume.description.description.c_str());
    ImGui::Dummy(ImVec2(0.f, 16.f));

    // ImGui::Text("Records count:  %ld", _volume.records.size());
    // ImGui::Dummy(ImVec2(0.f, 16.f));

    // nav
    if (ImGui::Button("Home"))
    {
        _volume_state->reset();
    }

    _draw_table();
    ImGui::End();
}

void FilesNavigator::_draw_table()
{

    ImGuiTableFlags table_flags = ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg;
    ImGuiTableColumnFlags column_name_flags = ImGuiTableColumnFlags_DefaultSort |
                                              ImGuiTableColumnFlags_WidthStretch;

    if (ImGui::BeginTable("files_list", 3, table_flags))
    {

        // header
        {
            ImGui::TableSetupColumn("File", column_name_flags, 1.0f);
            ImGui::TableSetupColumn("Size", column_name_flags, 0.2f);
            ImGui::TableSetupColumn("Date", column_name_flags, 0.2f);
            ImGui::TableHeadersRow();
        }

        // body
        for (domain::FileRecord fr : _get_files())
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

            // щелчок на строке - выглядит не очень... пока кнопки
            // // Переменная для подсветки выбранной строки (если нужно)
            // static uint64_t selected_row = 0;
            // bool is_selected = (selected_row == fr.id);

            // // Используем строку как уникальный ID для Selectable
            // char label[64];
            // sprintf(label, "##row_%d", fr.id);

            // if (ImGui::Selectable(label, is_selected, ImGuiSelectableFlags_AllowOverlap))
            // {
            //     selected_row = fr.id; // Запоминаем выбор

            //     // Здесь обрабатываем клик по строке!
            //     // Например, открываем окно, меняем стейт приложения и т.д.
            //     printf("Кликнули на строку: %d\n", fr.id);
            // }
            // ImGui::SameLine();

            ImGui::PushID(fr.id);
            if (ImGui::SmallButton("..."))
            {
                if (fr.ftype == domain::FTYPE_FOLDER)
                {
                    _volume_state->push(fr.id);
                }
            }
            ImGui::PopID();
            ImGui::SameLine();

            ImGui::Text("%s %s", currentIcon.data(), fr.name.c_str());

            ImGui::TableSetColumnIndex(column++);
            ImGui::Text("%ld", fr.size);

            ImGui::TableSetColumnIndex(column++);
            ImGui::Text("%ld", fr.time);

            // if (ImGui::IsItemClicked)
            // {
            //     std::cout << "clicked" << std::endl;
            // }
        }
        ImGui::EndTable();
    }
}

bool FilesNavigator::_open_volume()
{

    const std::string filePath = "/tmp/example-db";
    std::cout << "start open volume" << std::endl;

    _volume_provider->open(filePath);
    _volume_state->reset();

    return true;
}

std::vector<domain::FileRecord> FilesNavigator::_get_files()
{
    std::vector<domain::FileRecord> folders;
    std::vector<domain::FileRecord> files;
    std::vector<domain::FileRecord> unknown;

    for (domain::FileRecord fr : _volume_state->get_actual_items())
    {
        if (fr.ftype == domain::FTYPE_FOLDER)
        {
            folders.push_back(fr);
        }

        if (fr.ftype == domain::FTYPE_FILE)
        {
            files.push_back(fr);
        }

        if (fr.ftype != domain::FTYPE_FOLDER && fr.ftype != domain::FTYPE_FILE)
        {
            unknown.push_back(fr);
        }
    }

    std::vector<domain::FileRecord> result;
    for (auto fr : folders)
    {
        result.push_back(fr);
    }

    for (auto fr : files)
    {
        result.push_back(fr);
    }

    for (auto fr : unknown)
    {
        result.push_back(fr);
    }

    return result;
}