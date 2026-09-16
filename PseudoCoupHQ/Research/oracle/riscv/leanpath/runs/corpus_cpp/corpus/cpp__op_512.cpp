// probe 512 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_512(uint64_t a, uint64_t b)
{
    return a != b;
}
