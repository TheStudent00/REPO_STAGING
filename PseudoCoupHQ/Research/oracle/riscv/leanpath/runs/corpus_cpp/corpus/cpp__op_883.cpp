// probe 883 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_883(double a, int64_t b)
{
    return a bitor b;
}
