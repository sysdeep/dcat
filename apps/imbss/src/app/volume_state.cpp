#include "volume_state.hpp"

using namespace APP;

VolumeState::VolumeState(VolumeProvider *provider) : _provider(provider)
{

    reset();
}

std::vector<domain::FileRecord> VolumeState::get_child_items(uint64_t parent_id)
{

    std::vector<domain::FileRecord> result;
    for (auto fr : _provider->get_volume().records)
    {
        if (fr.parent == parent_id)
        {
            result.push_back(fr);
        }
    }

    return result;
}

std::vector<domain::FileRecord> VolumeState::get_actual_items()
{
    uint64_t id = _store.top();

    return get_child_items(id);
}

void VolumeState::push(uint64_t item_id)
{
    _store.push(item_id);
}

void VolumeState::reset()
{
    _store = std::stack<uint64_t>{};

    // NOTE: 0 - root of scan, 1 - files in root
    _store.push(1);
}

uint64_t VolumeState::pop()
{
    uint64_t id = _store.top();
    _store.pop();
    return id;
}