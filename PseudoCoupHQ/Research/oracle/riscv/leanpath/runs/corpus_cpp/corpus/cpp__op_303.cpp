// probe 303 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_303(float a, float b)
{
    return a || b;
}
