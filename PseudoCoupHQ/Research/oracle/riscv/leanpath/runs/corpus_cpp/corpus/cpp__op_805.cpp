// probe 805 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_805(float a, int64_t b)
{
    return a or b;
}
