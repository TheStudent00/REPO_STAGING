// probe 40 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_40(double a)
{
    return *a;
}
