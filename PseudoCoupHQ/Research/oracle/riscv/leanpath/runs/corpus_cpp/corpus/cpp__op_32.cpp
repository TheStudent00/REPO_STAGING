// probe 32 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_32(uint64_t a)
{
    return compl a;
}
