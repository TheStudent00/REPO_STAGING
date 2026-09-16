// probe 672 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_672(bool a, int32_t b)
{
    return a < b;
}
