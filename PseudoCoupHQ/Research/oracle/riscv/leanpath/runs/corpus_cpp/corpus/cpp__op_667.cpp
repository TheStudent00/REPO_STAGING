// probe 667 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_667(double a, int64_t b)
{
    return a < b;
}
