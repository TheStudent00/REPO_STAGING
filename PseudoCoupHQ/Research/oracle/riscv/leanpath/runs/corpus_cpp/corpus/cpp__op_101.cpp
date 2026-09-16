// probe 101 -- unary ...
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_101(bool a)
{
    return a...;
}
