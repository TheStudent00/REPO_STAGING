// probe 466 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_466(int32_t a, double b)
{
    return a == b;
}
