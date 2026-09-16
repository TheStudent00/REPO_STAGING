// probe 285 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_285(int32_t a, float b)
{
    return a || b;
}
