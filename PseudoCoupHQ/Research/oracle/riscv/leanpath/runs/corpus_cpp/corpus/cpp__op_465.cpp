// probe 465 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_465(int32_t a, float b)
{
    return a == b;
}
