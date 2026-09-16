// probe 879 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_879(float a, float b)
{
    return a bitor b;
}
