// probe 472 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_472(int64_t a, double b)
{
    return a == b;
}
