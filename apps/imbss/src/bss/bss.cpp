#include "bss.hpp"

std::vector<uint8_t> marshal(Volume &vol)
{

    BinaryWriter writer;

    write_header(writer, vol.header);

    return writer.buffer;
}

Volume unmarshal(const std::vector<uint8_t> &buffer)
{
    BinaryReader reader(buffer);

    FileHeader header = read_header(reader);
    VolumeDescription description = read_description(reader);

    std::vector<FileRecord> records;
    for (int i = 0; i < description.records; i++)
    {
        FileRecord record = read_record(reader);
        records.push_back(record);
    }

    return Volume{
        header,
        description,
        records,
    };
}

void write_header(BinaryWriter &writer, const FileHeader &header)
{
    writer.write_int(header.magic);
    writer.write_int(header.version);
}

FileHeader read_header(BinaryReader &reader)
{
    std::uint16_t magic = reader.read_int<std::uint16_t>();
    std::uint16_t version = reader.read_int<std::uint16_t>();

    return FileHeader{
        version,
        magic,
    };
}

VolumeDescription read_description(BinaryReader &reader)
{
    uint64_t created = reader.read_int<std::uint64_t>();
    uint16_t icon = reader.read_int<std::uint16_t>();
    uint64_t records = reader.read_int<std::uint64_t>();
    std::string name = reader.read_string();
    std::string scan_path = reader.read_string();
    std::string description = reader.read_string();

    return VolumeDescription{
        created,
        icon,
        records,
        name,
        scan_path,
        description,
    };
}

FileRecord read_record(BinaryReader &reader)
{

    // NOTE: порядок важен!!!
    uint64_t id = reader.read_int<uint64_t>();
    uint64_t parent = reader.read_int<uint64_t>();
    uint64_t size = reader.read_int<uint64_t>();
    uint16_t ftype = reader.read_int<uint16_t>();
    uint64_t time = reader.read_int<uint64_t>();
    std::string name = reader.read_string();

    return FileRecord{
        id,
        parent,
        size,
        time,
        ftype,
        name,
    };
}

// std::vector<FileRecord> read_records(BinaryReader &reader)
// {
//     reader.read_vector();
// }