// probe 874 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_874(uint64_t a, double b)
{
    return a bitor b;
}
