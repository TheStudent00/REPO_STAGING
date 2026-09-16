// probe 865 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_865(int64_t a, int64_t b)
{
    return a bitor b;
}
