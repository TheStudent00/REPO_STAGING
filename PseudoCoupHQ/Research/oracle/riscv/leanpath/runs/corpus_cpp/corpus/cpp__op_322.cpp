// probe 322 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_322(int32_t a, double b)
{
    return a && b;
}
