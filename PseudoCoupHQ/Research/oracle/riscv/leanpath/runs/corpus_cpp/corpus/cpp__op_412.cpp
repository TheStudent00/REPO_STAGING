// probe 412 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_412(float a, double b)
{
    return a ^ b;
}
