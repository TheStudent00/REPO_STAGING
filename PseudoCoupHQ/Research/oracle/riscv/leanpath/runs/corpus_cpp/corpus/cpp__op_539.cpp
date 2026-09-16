// probe 539 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_539(int32_t a, bool b)
{
    return a > b;
}
