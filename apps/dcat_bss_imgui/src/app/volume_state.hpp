#pragma once
#include <vector>
#include <stack>
#include "domain/volume.hpp"
#include "volume_provider.hpp"

namespace APP
{
    class VolumeState
    {
    public:
        VolumeState(VolumeProvider *provider);

        std::vector<domain::FileRecord> get_child_items(uint64_t parent_id);
        std::vector<domain::FileRecord> get_actual_items();
        void push(uint64_t item_id);
        void reset();
        uint64_t pop();

    private:
        VolumeProvider *_provider;
        std::stack<uint64_t> _store;
    };
}