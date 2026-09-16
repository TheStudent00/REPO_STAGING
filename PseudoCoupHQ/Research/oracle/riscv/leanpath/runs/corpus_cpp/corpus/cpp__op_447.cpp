// probe 447 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_447(float a, float b)
{
    return a & b;
}
