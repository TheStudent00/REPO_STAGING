// probe 82 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_82(double a)
{
    return delete a;
}
