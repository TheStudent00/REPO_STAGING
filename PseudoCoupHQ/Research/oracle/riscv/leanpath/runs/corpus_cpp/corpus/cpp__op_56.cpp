// probe 56 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_56(uint64_t a)
{
    return --a;
}
