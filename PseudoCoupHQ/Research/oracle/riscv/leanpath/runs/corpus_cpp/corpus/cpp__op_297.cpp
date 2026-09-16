// probe 297 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_297(uint64_t a, float b)
{
    return a || b;
}
