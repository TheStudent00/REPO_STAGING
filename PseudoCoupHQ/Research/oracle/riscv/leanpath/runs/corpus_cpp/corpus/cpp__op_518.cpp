// probe 518 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_518(float a, uint64_t b)
{
    return a != b;
}
