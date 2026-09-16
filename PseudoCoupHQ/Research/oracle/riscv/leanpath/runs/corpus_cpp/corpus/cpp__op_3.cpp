// probe 3 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_3(float a)
{
    return !a;
}
