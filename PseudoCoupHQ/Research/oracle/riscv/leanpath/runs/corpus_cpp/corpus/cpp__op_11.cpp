// probe 11 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_11(bool a)
{
    return ~a;
}
