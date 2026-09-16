// probe 127 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_127(double a, int64_t b)
{
    return a + b;
}
