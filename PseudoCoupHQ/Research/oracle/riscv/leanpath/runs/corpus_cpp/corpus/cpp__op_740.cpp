// probe 740 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_740(double a, uint64_t b)
{
    return a >> b;
}
