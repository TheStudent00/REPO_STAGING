// probe 38 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_38(uint64_t a)
{
    return *a;
}
