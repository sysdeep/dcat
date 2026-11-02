#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace bss
{

    struct FileHeader
    {
        uint16_t version;
        uint16_t magic;
    };

    struct VolumeDescription
    {
        uint64_t created;
        uint16_t icon;
        uint64_t records;
        std::string name;
        std::string scan_path;
        std::string description;
    };

    struct FileRecord
    {
        uint64_t id;
        uint64_t parent;
        uint64_t size;
        uint64_t time;
        uint16_t ftype;
        std::string name;
    };

    struct Volume
    {
        FileHeader header;
        VolumeDescription description;
        std::vector<FileRecord> records;
    };
}