// probe 391 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_391(int32_t a, int64_t b)
{
    return a ^ b;
}
