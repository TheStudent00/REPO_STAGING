// probe 419 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_419(double a, bool b)
{
    return a ^ b;
}
