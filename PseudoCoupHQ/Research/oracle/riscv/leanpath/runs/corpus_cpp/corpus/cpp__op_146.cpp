// probe 146 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_146(int64_t a, uint64_t b)
{
    return a - b;
}
