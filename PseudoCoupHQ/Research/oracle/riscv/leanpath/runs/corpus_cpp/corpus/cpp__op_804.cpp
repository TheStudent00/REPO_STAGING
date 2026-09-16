// probe 804 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_804(float a, int32_t b)
{
    return a or b;
}
