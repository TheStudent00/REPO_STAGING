// probe 417 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_417(double a, float b)
{
    return a ^ b;
}
