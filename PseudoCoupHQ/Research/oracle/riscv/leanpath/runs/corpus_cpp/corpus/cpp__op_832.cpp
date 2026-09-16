// probe 832 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_832(int64_t a, double b)
{
    return a and b;
}
