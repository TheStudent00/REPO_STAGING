// probe 399 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_399(int64_t a, float b)
{
    return a ^ b;
}
