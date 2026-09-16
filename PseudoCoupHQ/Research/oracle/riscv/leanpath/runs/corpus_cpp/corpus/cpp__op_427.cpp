// probe 427 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_427(int32_t a, int64_t b)
{
    return a & b;
}
