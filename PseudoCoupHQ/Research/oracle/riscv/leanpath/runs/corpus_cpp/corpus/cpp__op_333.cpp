// probe 333 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_333(uint64_t a, float b)
{
    return a && b;
}
