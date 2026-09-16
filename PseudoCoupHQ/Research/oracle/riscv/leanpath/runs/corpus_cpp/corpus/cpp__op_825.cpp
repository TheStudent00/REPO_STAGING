// probe 825 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_825(int32_t a, float b)
{
    return a and b;
}
