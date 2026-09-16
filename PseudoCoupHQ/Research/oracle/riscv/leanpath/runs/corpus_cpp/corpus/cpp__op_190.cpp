// probe 190 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_190(uint64_t a, double b)
{
    return a * b;
}
