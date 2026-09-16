// probe 837 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_837(uint64_t a, float b)
{
    return a and b;
}
