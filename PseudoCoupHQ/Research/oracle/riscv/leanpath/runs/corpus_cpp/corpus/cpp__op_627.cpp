// probe 627 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_627(float a, float b)
{
    return a <= b;
}
