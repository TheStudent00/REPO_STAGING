// probe 573 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_573(int32_t a, float b)
{
    return a >= b;
}
