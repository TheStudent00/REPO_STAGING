// probe 888 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_888(bool a, int32_t b)
{
    return a bitor b;
}
