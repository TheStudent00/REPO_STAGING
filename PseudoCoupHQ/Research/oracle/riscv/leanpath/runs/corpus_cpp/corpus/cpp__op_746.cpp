// probe 746 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_746(bool a, uint64_t b)
{
    return a >> b;
}
