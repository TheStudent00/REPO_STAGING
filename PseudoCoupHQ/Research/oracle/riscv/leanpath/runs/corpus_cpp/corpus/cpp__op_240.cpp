// probe 240 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_240(bool a, int32_t b)
{
    return a / b;
}
