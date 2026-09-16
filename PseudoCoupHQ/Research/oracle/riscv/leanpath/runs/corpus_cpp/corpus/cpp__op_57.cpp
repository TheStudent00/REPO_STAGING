// probe 57 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_57(float a)
{
    return --a;
}
