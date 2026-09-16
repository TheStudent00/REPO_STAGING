// probe 7 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_7(int64_t a)
{
    return ~a;
}
