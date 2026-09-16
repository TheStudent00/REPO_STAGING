// probe 415 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_415(double a, int64_t b)
{
    return a ^ b;
}
