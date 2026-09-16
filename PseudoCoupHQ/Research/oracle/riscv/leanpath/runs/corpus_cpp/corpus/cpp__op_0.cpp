// probe 0 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_0(int32_t a)
{
    return !a;
}
