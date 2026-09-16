// probe 884 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_884(double a, uint64_t b)
{
    return a bitor b;
}
