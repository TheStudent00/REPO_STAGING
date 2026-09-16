// probe 327 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_327(int64_t a, float b)
{
    return a && b;
}
