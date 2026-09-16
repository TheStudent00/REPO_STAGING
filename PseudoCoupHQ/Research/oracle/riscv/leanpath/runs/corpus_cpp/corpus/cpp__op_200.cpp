// probe 200 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_200(double a, uint64_t b)
{
    return a * b;
}
