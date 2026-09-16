// probe 39 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_39(float a)
{
    return *a;
}
