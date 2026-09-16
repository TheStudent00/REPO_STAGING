// probe 21 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_21(float a)
{
    return +a;
}
