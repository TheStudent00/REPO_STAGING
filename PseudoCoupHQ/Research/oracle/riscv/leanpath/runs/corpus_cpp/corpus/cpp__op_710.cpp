// probe 710 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_710(bool a, uint64_t b)
{
    return a << b;
}
