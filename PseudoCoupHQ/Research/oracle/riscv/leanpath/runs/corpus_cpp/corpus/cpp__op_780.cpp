// probe 780 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_780(bool a, int32_t b)
{
    return a <=> b;
}
