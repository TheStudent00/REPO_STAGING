// probe 639 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_639(bool a, float b)
{
    return a <= b;
}
