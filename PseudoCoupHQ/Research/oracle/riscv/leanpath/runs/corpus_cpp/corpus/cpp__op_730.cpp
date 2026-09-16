// probe 730 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_730(uint64_t a, double b)
{
    return a >> b;
}
