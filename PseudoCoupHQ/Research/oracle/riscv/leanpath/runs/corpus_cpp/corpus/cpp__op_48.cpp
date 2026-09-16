// probe 48 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_48(int32_t a)
{
    return ++a;
}
