// probe 567 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_567(bool a, float b)
{
    return a > b;
}
