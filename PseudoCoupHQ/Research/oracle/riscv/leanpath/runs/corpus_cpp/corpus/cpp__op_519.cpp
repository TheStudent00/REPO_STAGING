// probe 519 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_519(float a, float b)
{
    return a != b;
}
