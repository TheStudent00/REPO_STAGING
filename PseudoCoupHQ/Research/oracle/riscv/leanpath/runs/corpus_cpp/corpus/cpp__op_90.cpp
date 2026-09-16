// probe 90 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_90(int32_t a)
{
    return a--;
}
