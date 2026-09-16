// probe 488 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_488(double a, uint64_t b)
{
    return a == b;
}
