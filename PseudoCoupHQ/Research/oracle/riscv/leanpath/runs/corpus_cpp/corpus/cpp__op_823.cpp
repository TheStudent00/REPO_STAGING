// probe 823 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_823(int32_t a, int64_t b)
{
    return a and b;
}
