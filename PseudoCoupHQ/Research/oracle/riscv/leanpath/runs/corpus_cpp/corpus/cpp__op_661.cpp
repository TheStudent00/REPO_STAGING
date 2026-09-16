// probe 661 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_661(float a, int64_t b)
{
    return a < b;
}
