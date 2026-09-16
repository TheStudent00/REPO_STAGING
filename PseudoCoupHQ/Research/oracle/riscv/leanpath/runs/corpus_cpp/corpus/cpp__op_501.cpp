// probe 501 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_501(int32_t a, float b)
{
    return a != b;
}
