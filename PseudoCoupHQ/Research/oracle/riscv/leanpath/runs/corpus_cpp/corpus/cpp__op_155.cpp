// probe 155 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_155(uint64_t a, bool b)
{
    return a - b;
}
