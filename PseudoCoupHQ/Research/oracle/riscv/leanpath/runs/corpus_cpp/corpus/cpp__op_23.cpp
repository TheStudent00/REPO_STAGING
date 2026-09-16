// probe 23 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_23(bool a)
{
    return +a;
}
