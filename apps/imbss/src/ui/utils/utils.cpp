#include "imgui.h"
#include "utils.hpp"

// void UI::CenterTextInCell(const std::string &text)
void UI::CenterTextInCell(const char *text)
{
    // Calculate the width of the text
    float textWidth = ImGui::CalcTextSize(text).x;

    // Get the current column width
    float columnWidth = ImGui::GetColumnWidth(); // Or use ImGui::TableGetColumnWidth() inside a table

    // Calculate the indentation needed to center the text
    float indentation = (columnWidth - textWidth) * 0.5f;

    // Optional: Add some minimum indentation to prevent issues with very long text
    if (indentation < 0.0f)
        indentation = 0.0f;

    // Set the cursor position for horizontal centering.
    // Need to account for the current cursor X position as SetCursorPosX is absolute to the window/table, not the column start.
    // A better approach in a table is to use the current column's starting position:
    float startX = ImGui::GetCursorPosX();
    ImGui::SetCursorPosX(startX + indentation);

    ImGui::Text("%s", text);
}