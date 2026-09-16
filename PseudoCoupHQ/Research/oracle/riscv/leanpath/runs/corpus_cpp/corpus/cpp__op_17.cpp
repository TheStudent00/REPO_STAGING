// probe 17 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_17(bool a)
{
    return -a;
}
