// probe 394 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_394(int32_t a, double b)
{
    return a ^ b;
}
