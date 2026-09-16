// probe 633 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_633(double a, float b)
{
    return a <= b;
}
