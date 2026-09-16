// probe 45 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_45(float a)
{
    return &a;
}
