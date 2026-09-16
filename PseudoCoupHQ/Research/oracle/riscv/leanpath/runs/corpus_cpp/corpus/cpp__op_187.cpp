// probe 187 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_187(uint64_t a, int64_t b)
{
    return a * b;
}
