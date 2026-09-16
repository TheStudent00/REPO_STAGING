// probe 430 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_430(int32_t a, double b)
{
    return a & b;
}
