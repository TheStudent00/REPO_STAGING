// probe 286 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_286(int32_t a, double b)
{
    return a || b;
}
