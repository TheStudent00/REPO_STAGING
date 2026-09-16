// probe 76 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_76(double a)
{
    return new a;
}
