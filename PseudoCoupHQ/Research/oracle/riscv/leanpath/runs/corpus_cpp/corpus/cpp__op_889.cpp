// probe 889 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_889(bool a, int64_t b)
{
    return a bitor b;
}
