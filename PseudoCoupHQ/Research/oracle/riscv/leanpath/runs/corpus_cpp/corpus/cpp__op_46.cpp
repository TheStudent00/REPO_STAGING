// probe 46 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_46(double a)
{
    return &a;
}
