// probe 27 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_27(float a)
{
    return not a;
}
