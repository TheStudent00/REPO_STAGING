// probe 12 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_12(int32_t a)
{
    return -a;
}
