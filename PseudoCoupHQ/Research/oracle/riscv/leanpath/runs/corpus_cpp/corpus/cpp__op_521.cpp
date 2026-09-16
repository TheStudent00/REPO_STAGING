// probe 521 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_521(float a, bool b)
{
    return a != b;
}
