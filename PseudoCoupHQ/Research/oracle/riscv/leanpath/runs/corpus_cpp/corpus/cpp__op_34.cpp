// probe 34 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_34(double a)
{
    return compl a;
}
