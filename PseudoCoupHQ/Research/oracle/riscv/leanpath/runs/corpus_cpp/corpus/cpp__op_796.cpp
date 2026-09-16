// probe 796 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_796(int64_t a, double b)
{
    return a or b;
}
