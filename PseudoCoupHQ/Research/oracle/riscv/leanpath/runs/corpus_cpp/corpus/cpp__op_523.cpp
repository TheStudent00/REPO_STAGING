// probe 523 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_523(double a, int64_t b)
{
    return a != b;
}
