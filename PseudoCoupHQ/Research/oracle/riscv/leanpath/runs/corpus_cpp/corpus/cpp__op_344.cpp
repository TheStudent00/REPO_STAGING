// probe 344 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_344(double a, uint64_t b)
{
    return a && b;
}
