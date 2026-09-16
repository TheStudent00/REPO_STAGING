// probe 508 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_508(int64_t a, double b)
{
    return a != b;
}
