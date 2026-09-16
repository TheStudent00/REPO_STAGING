// probe 93 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_93(float a)
{
    return a--;
}
