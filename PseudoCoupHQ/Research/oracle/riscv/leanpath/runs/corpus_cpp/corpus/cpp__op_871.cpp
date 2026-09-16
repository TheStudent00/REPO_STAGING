// probe 871 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_871(uint64_t a, int64_t b)
{
    return a bitor b;
}
