// probe 86 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_86(uint64_t a)
{
    return a++;
}
