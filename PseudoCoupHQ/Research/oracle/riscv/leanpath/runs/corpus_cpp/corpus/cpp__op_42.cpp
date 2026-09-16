// probe 42 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_42(int32_t a)
{
    return &a;
}
