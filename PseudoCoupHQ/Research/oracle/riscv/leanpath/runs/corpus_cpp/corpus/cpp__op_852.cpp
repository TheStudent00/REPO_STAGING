// probe 852 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_852(bool a, int32_t b)
{
    return a and b;
}
