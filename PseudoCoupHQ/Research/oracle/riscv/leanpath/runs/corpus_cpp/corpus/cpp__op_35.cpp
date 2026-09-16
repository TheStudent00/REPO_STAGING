// probe 35 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_35(bool a)
{
    return compl a;
}
