// probe 734 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_734(float a, uint64_t b)
{
    return a >> b;
}
