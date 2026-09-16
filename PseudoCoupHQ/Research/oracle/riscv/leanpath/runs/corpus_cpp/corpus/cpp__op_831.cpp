// probe 831 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_831(int64_t a, float b)
{
    return a and b;
}
