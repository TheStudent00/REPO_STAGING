// probe 824 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_824(int32_t a, uint64_t b)
{
    return a and b;
}
