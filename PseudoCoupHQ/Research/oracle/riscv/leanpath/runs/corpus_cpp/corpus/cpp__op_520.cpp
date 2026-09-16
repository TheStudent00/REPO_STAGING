// probe 520 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_520(float a, double b)
{
    return a != b;
}
