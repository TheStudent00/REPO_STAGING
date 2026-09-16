// probe 81 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_81(float a)
{
    return delete a;
}
