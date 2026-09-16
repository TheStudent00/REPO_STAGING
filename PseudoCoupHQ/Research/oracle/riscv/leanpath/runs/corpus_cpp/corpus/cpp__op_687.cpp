// probe 687 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_687(int64_t a, float b)
{
    return a << b;
}
