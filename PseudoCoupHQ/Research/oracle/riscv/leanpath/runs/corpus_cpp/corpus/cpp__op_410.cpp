// probe 410 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_410(float a, uint64_t b)
{
    return a ^ b;
}
