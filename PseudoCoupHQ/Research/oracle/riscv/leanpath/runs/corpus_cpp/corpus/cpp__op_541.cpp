// probe 541 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_541(int64_t a, int64_t b)
{
    return a > b;
}
