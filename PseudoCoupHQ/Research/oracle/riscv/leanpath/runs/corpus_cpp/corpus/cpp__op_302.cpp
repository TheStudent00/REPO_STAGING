// probe 302 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_302(float a, uint64_t b)
{
    return a || b;
}
