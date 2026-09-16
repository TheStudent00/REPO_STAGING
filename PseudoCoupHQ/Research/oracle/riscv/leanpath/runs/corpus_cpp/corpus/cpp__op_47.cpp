// probe 47 -- unary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_47(bool a)
{
    return &a;
}
