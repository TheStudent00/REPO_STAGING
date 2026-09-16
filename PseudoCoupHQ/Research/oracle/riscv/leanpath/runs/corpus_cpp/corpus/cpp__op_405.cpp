// probe 405 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_405(uint64_t a, float b)
{
    return a ^ b;
}
