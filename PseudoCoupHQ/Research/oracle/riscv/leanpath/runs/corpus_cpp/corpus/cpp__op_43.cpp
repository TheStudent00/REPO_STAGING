// probe 43 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_43(int64_t a)
{
    return &a;
}
