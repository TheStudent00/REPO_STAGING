// probe 514 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_514(uint64_t a, double b)
{
    return a != b;
}
