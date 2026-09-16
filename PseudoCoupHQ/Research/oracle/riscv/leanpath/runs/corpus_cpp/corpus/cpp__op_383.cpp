// probe 383 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_383(double a, bool b)
{
    return a | b;
}
