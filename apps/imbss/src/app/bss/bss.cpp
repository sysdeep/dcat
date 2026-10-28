#include "bss.hpp"

namespace bss
{
    // std::vector<uint8_t> marshal(Volume &vol)
    // {

    //     BinaryWriter writer;

    //     write_header(writer, vol.header);

    //     return writer.buffer;
    // }

    domain::Volume unmarshal(const std::vector<uint8_t> &buffer)
    {
        BinaryReader reader(buffer);

        // header
        std::uint16_t magic = reader.read_int<std::uint16_t>();
        std::uint16_t version = reader.read_int<std::uint16_t>();
        domain::VolumeMeta meta{
            version,
            magic,
        };

        // volume description
        uint64_t created = reader.read_int<std::uint64_t>();
        uint16_t icon = reader.read_int<std::uint16_t>();
        uint64_t records_count = reader.read_int<std::uint64_t>();
        std::string name = reader.read_string();
        std::string scan_path = reader.read_string();
        std::string description = reader.read_string();

        domain::VolumeDescription volume_description{
            created,
            icon,
            records_count,
            name,
            scan_path,
            description,
        };

        // file records
        std::vector<domain::FileRecord> records;
        for (int i = 0; i < records_count; i++)
        {
            domain::FileRecord record = read_record(reader);
            records.push_back(record);
        }

        return domain::Volume{
            meta,
            volume_description,
            records,
        };
    }

    // void write_header(BinaryWriter &writer, const FileHeader &header)
    // {
    //     writer.write_int(header.magic);
    //     writer.write_int(header.version);
    // }

    // FileHeader read_header(BinaryReader &reader)
    // {
    //     std::uint16_t magic = reader.read_int<std::uint16_t>();
    //     std::uint16_t version = reader.read_int<std::uint16_t>();

    //     return FileHeader{
    //         version,
    //         magic,
    //     };
    // }

    // VolumeDescription read_description(BinaryReader &reader)
    // {
    //     uint64_t created = reader.read_int<std::uint64_t>();
    //     uint16_t icon = reader.read_int<std::uint16_t>();
    //     uint64_t records = reader.read_int<std::uint64_t>();
    //     std::string name = reader.read_string();
    //     std::string scan_path = reader.read_string();
    //     std::string description = reader.read_string();

    //     return VolumeDescription{
    //         created,
    //         icon,
    //         records,
    //         name,
    //         scan_path,
    //         description,
    //     };
    // }

    domain::FileRecord read_record(BinaryReader &reader)
    {

        // NOTE: порядок важен!!!
        uint64_t id = reader.read_int<uint64_t>();
        uint64_t parent = reader.read_int<uint64_t>();
        uint64_t size = reader.read_int<uint64_t>();
        uint16_t ftype = reader.read_int<uint16_t>();
        uint64_t time = reader.read_int<uint64_t>();
        std::string name = reader.read_string();

        return domain::FileRecord{
            id,
            parent,
            size,
            time,
            ftype,
            name,
        };
    }

}