// probe 29 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_29(bool a)
{
    return not a;
}
