// probe 487 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_487(double a, int64_t b)
{
    return a == b;
}
