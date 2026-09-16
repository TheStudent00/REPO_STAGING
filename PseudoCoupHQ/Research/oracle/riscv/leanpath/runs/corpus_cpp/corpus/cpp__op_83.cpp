// probe 83 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_83(bool a)
{
    return delete a;
}
