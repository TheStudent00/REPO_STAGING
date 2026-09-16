// probe 697 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_697(float a, int64_t b)
{
    return a << b;
}
