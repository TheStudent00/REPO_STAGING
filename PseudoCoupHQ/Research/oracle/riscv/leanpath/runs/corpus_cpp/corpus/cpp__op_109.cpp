// probe 109 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_109(int64_t a, int64_t b)
{
    return a + b;
}
