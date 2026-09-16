// probe 674 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_674(bool a, uint64_t b)
{
    return a < b;
}
