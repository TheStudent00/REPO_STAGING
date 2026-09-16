// probe 668 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_668(double a, uint64_t b)
{
    return a < b;
}
