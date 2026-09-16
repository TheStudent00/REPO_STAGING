// probe 688 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_688(int64_t a, double b)
{
    return a << b;
}
