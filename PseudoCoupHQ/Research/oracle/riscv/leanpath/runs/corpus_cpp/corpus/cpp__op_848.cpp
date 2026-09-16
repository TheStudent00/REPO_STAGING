// probe 848 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_848(double a, uint64_t b)
{
    return a and b;
}
