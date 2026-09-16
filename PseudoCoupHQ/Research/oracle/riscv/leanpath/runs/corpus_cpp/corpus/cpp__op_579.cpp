// probe 579 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_579(int64_t a, float b)
{
    return a >= b;
}
