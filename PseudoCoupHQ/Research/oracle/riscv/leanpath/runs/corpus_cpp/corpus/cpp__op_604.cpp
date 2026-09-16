// probe 604 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_604(bool a, double b)
{
    return a >= b;
}
