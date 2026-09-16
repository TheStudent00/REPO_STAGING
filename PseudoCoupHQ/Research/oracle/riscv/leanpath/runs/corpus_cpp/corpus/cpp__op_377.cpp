// probe 377 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_377(float a, bool b)
{
    return a | b;
}
