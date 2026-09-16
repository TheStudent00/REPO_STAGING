// probe 182 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_182(int64_t a, uint64_t b)
{
    return a * b;
}
