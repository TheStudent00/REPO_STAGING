// probe 33 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_33(float a)
{
    return compl a;
}
