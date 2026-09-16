// probe 443 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_443(uint64_t a, bool b)
{
    return a & b;
}
