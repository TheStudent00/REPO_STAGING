// probe 121 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_121(float a, int64_t b)
{
    return a + b;
}
