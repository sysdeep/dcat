#include "volume_provider.hpp"
#include "gzip_reader.hpp"
#include "app/bss/bss.hpp"

using namespace APP;

VolumeProvider::VolumeProvider() {}

bool VolumeProvider::open(std::string filePath)
{

    std::vector<uint8_t> buffer;

    if (readGzipToBuffer(filePath, buffer))
    {
        _volume = bss::unmarshal(buffer);

        // std::cout << "Volume header version: " << _volume.header.version << std::endl;
        // std::cout << "Volume header magic: " << _volume.header.magic << std::endl;

        // std::cout << "Volume created: " << _volume.description.created << std::endl;
        // std::cout << "Volume icon: " << _volume.description.icon << std::endl;
        // std::cout << "Volume records: " << _volume.description.records << std::endl;
        // std::cout << "Volume name: " << _volume.description.name << std::endl;
        // std::cout << "Volume scan_path: " << _volume.description.scan_path << std::endl;
        // std::cout << "Volume description: " << _volume.description.description << std::endl;
        return true;
    }
    else
    {
        std::cerr << "Unable read " << std::endl;
        return false;
    }
}

domain::Volume &VolumeProvider::get_volume()
{
    return _volume;
}
