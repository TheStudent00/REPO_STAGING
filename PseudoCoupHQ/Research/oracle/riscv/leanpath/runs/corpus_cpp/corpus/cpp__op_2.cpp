// probe 2 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_2(uint64_t a)
{
    return !a;
}
