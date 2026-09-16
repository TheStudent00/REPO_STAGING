// probe 301 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_301(float a, int64_t b)
{
    return a || b;
}
