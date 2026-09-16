// probe 5 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_5(bool a)
{
    return !a;
}
