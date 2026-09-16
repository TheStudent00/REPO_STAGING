// probe 22 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_22(double a)
{
    return +a;
}
