// probe 418 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_418(double a, double b)
{
    return a ^ b;
}
