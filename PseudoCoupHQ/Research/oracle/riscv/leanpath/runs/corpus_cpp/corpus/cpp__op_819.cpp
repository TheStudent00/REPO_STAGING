// probe 819 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_819(bool a, float b)
{
    return a or b;
}
