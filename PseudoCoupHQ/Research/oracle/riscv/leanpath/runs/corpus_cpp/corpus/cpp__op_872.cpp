// probe 872 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_872(uint64_t a, uint64_t b)
{
    return a bitor b;
}
