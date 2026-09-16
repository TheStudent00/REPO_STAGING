// probe 406 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_406(uint64_t a, double b)
{
    return a ^ b;
}
