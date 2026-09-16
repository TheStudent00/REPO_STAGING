// probe 292 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_292(int64_t a, double b)
{
    return a || b;
}
