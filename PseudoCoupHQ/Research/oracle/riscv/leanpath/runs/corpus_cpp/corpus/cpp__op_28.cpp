// probe 28 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_28(double a)
{
    return not a;
}
