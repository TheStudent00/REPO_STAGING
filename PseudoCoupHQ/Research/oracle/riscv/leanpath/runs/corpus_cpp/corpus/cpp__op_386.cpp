// probe 386 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_386(bool a, uint64_t b)
{
    return a | b;
}
