// probe 600 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_600(bool a, int32_t b)
{
    return a >= b;
}
