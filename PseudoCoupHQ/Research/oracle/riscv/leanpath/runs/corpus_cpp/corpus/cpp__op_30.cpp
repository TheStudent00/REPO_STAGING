// probe 30 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_30(int32_t a)
{
    return compl a;
}
