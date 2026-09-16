// probe 37 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_37(int64_t a)
{
    return *a;
}
