// probe 532 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_532(bool a, double b)
{
    return a != b;
}
