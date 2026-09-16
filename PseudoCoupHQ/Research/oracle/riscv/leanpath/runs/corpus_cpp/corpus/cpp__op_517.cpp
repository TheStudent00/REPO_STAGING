// probe 517 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_517(float a, int64_t b)
{
    return a != b;
}
