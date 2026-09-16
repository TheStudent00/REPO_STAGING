// probe 230 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_230(float a, uint64_t b)
{
    return a / b;
}
