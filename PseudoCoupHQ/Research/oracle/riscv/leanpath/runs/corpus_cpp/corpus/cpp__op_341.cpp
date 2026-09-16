// probe 341 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_341(float a, bool b)
{
    return a && b;
}
