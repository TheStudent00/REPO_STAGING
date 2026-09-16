// probe 611 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_611(int32_t a, bool b)
{
    return a <= b;
}
