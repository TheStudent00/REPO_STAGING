// probe 36 -- unary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_36(int32_t a)
{
    return *a;
}
