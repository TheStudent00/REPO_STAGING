// probe 189 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_189(uint64_t a, float b)
{
    return a * b;
}
