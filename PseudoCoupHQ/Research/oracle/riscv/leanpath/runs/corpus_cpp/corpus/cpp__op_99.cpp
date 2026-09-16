// probe 99 -- unary ...
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_99(float a)
{
    return a...;
}
