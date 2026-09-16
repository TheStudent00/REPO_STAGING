// probe 364 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_364(int64_t a, double b)
{
    return a | b;
}
