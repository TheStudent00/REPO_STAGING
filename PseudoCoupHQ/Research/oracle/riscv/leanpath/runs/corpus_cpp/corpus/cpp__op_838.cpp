// probe 838 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_838(uint64_t a, double b)
{
    return a and b;
}
