// probe 648 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_648(int64_t a, int32_t b)
{
    return a < b;
}
