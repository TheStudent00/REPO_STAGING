// probe 854 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_854(bool a, uint64_t b)
{
    return a and b;
}
