// probe 543 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_543(int64_t a, float b)
{
    return a > b;
}
