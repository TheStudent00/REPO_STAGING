// probe 220 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_220(int64_t a, double b)
{
    return a / b;
}
