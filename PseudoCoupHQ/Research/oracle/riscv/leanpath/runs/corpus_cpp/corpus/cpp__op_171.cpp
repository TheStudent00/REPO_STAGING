// probe 171 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_171(bool a, float b)
{
    return a - b;
}
