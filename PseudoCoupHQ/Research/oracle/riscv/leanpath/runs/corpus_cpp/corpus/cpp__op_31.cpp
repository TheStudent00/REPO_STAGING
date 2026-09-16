// probe 31 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_31(int64_t a)
{
    return compl a;
}
