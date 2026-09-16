// probe 75 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_75(float a)
{
    return new a;
}
