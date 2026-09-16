// probe 843 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_843(float a, float b)
{
    return a and b;
}
