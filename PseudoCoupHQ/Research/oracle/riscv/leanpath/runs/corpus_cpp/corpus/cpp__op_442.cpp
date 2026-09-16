// probe 442 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_442(uint64_t a, double b)
{
    return a & b;
}
