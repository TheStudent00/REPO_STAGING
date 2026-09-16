// probe 380 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_380(double a, uint64_t b)
{
    return a | b;
}
