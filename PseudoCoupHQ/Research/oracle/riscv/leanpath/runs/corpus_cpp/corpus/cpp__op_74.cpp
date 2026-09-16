// probe 74 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_74(uint64_t a)
{
    return new a;
}
