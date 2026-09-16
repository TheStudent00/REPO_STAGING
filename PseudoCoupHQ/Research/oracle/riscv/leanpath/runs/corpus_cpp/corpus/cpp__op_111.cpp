// probe 111 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_111(int64_t a, float b)
{
    return a + b;
}
