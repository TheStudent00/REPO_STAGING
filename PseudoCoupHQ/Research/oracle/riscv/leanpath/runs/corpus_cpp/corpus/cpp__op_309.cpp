// probe 309 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_309(double a, float b)
{
    return a || b;
}
