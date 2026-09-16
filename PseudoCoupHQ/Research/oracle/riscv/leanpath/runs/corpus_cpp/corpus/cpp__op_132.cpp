// probe 132 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_132(bool a, int32_t b)
{
    return a + b;
}
