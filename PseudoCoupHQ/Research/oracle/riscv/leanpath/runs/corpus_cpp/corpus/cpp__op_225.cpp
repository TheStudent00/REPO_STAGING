// probe 225 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_225(uint64_t a, float b)
{
    return a / b;
}
