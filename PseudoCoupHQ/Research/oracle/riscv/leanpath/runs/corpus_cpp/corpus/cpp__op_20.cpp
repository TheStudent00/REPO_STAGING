// probe 20 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_20(uint64_t a)
{
    return +a;
}
