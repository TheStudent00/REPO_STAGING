// probe 298 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_298(uint64_t a, double b)
{
    return a || b;
}
