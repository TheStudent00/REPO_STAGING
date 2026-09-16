// probe 162 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_162(double a, int32_t b)
{
    return a - b;
}
