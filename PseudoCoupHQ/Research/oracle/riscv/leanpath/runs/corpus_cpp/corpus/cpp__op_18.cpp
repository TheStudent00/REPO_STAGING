// probe 18 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_18(int32_t a)
{
    return +a;
}
