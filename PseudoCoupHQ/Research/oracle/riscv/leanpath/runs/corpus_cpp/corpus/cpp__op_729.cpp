// probe 729 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_729(uint64_t a, float b)
{
    return a >> b;
}
