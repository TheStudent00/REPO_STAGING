// probe 4 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_4(double a)
{
    return !a;
}
