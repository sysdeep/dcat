#pragma once
#include "model.hpp"
#include "vector"
#include "cstdint"
#include "binary_writer.hpp"
#include "binary_reader.hpp"

std::vector<uint8_t> marshal(Volume &vol);
Volume unmarshal(const std::vector<uint8_t> &buffer);

// private

void write_header(BinaryWriter &writer, const FileHeader &header);
FileHeader read_header(BinaryReader &reader);
VolumeDescription read_description(BinaryReader &reader);

FileRecord read_record(BinaryReader &reader);
// std::vector<FileRecord> read_records(BinaryReader &reader);