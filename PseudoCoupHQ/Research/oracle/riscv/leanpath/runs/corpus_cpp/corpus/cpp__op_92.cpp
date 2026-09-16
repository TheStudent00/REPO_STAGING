// probe 92 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_92(uint64_t a)
{
    return a--;
}
