// probe 85 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_85(int64_t a)
{
    return a++;
}
