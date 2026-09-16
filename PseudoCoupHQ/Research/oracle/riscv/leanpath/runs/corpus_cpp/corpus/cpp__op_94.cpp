// probe 94 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_94(double a)
{
    return a--;
}
