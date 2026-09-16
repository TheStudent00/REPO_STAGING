// probe 704 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_704(double a, uint64_t b)
{
    return a << b;
}
