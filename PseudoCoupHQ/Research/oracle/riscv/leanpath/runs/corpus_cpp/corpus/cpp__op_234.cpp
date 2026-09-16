// probe 234 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_234(double a, int32_t b)
{
    return a / b;
}
