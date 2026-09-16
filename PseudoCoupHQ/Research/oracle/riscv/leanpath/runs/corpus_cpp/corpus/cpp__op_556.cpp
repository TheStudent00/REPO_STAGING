// probe 556 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_556(float a, double b)
{
    return a > b;
}
