// probe 339 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_339(float a, float b)
{
    return a && b;
}
