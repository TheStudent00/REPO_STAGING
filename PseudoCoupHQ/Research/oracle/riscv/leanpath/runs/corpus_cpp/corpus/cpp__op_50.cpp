// probe 50 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_50(uint64_t a)
{
    return ++a;
}
