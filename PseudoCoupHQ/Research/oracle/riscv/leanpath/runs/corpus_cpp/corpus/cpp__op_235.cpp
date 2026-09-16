// probe 235 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_235(double a, int64_t b)
{
    return a / b;
}
