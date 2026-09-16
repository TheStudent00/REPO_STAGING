// probe 828 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_828(int64_t a, int32_t b)
{
    return a and b;
}
