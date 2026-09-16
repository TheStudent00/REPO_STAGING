// probe 658 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_658(uint64_t a, double b)
{
    return a < b;
}
