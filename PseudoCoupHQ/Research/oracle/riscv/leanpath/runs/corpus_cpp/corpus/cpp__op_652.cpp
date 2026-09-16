// probe 652 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_652(int64_t a, double b)
{
    return a < b;
}
