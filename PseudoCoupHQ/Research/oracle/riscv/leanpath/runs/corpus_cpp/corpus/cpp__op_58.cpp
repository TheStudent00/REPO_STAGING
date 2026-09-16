// probe 58 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_58(double a)
{
    return --a;
}
