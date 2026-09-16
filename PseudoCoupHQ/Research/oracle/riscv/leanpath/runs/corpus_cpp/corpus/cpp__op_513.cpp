// probe 513 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_513(uint64_t a, float b)
{
    return a != b;
}
