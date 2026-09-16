// probe 726 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_726(uint64_t a, int32_t b)
{
    return a >> b;
}
