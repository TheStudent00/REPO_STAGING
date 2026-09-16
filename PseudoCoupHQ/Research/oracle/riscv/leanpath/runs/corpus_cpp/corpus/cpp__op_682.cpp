// probe 682 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_682(int32_t a, double b)
{
    return a << b;
}
