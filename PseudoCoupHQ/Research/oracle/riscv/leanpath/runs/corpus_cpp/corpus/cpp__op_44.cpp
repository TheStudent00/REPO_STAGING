// probe 44 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_44(uint64_t a)
{
    return &a;
}
