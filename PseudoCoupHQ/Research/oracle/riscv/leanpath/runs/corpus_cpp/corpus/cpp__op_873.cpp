// probe 873 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_873(uint64_t a, float b)
{
    return a bitor b;
}
