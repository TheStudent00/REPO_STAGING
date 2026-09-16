// probe 428 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_428(int32_t a, uint64_t b)
{
    return a & b;
}
