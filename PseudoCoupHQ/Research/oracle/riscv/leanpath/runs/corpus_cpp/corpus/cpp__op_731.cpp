// probe 731 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_731(uint64_t a, bool b)
{
    return a >> b;
}
