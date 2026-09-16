// probe 492 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_492(bool a, int32_t b)
{
    return a == b;
}
