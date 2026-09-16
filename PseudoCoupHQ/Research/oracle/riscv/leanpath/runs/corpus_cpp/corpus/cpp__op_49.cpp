// probe 49 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_49(int64_t a)
{
    return ++a;
}
