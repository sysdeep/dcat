#pragma once
#include "domain/volume.hpp"
#include "vector"
#include "cstdint"
#include "binary_writer.hpp"
#include "binary_reader.hpp"

namespace bss
{

    // class BssEncoder
    // {
    // public:
    //     BssEncoder();
    //     Volume unmarshal(const std::vector<uint8_t> &buffer);
    //     std::vector<uint8_t> marshal(Volume &vol);
    // };

    // std::vector<uint8_t> marshal(Volume &vol);
    domain::Volume unmarshal(const std::vector<uint8_t> &buffer);

    // private

    // void write_header(BinaryWriter &writer, const FileHeader &header);
    // FileHeader read_header(BinaryReader &reader);
    // VolumeDescription read_description(BinaryReader &reader);

    domain::FileRecord read_record(BinaryReader &reader);
    // std::vector<FileRecord> read_records(BinaryReader &reader);

}