// probe 334 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_334(uint64_t a, double b)
{
    return a && b;
}
