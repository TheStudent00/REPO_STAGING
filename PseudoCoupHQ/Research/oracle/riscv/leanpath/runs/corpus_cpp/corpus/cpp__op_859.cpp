// probe 859 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_859(int32_t a, int64_t b)
{
    return a bitor b;
}
