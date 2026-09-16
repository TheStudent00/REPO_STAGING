// probe 862 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_862(int32_t a, double b)
{
    return a bitor b;
}
