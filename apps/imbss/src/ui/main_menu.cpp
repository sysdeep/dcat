#include "./main_menu.hpp"
#include "imgui.h"

using namespace UI;

MainMenu::MainMenu() {}

void MainMenu::draw() {
    if (ImGui::BeginMainMenuBar()) {
        if (ImGui::BeginMenu("File")) {

            if (ImGui::MenuItem("Help", "CTRL+H")) {

                // show_help_window = true;
            }

            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu("Edit")) {
            if (ImGui::MenuItem("Undo", "CTRL+Z")) {
            }
            if (ImGui::MenuItem("Redo", "CTRL+Y", false, false)) {
            } // Disabled item
            ImGui::Separator();
            if (ImGui::MenuItem("Cut", "CTRL+X")) {
            }
            if (ImGui::MenuItem("Copy", "CTRL+C")) {
            }
            if (ImGui::MenuItem("Paste", "CTRL+V")) {
            }
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu("Debug")) {
            if (ImGui::MenuItem("Demo")) {
                this->_show_demo = !this->_show_demo;
            }
            ImGui::EndMenu();
        }
        ImGui::EndMainMenuBar();
    }

    if (this->_show_demo) {
        ImGui::ShowDemoWindow(&this->_show_demo);
    }
}
