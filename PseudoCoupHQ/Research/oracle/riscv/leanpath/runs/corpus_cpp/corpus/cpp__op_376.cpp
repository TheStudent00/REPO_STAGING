// probe 376 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_376(float a, double b)
{
    return a | b;
}
