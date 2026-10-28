#pragma once
#include <string_view>

namespace UI
{
    namespace Icons
    {
        // old cpp
        // constexpr const char *FolderCStr = u8"\uf07b";

        // В C++17/20 еще удобнее использовать string_view:
        constexpr std::string_view Folder = u8"\uf07b";
        constexpr std::string_view File = u8"\uea7b";
        constexpr std::string_view Search = u8"\uf002";
    }
}