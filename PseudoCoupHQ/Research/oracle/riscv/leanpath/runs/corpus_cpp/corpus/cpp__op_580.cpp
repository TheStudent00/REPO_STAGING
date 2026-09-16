// probe 580 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_580(int64_t a, double b)
{
    return a >= b;
}
