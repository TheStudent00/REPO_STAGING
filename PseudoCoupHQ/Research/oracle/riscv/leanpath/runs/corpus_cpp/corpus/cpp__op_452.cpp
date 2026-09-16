// probe 452 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_452(double a, uint64_t b)
{
    return a & b;
}
