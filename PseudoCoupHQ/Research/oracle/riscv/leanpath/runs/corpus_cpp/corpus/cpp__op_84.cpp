// probe 84 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_84(int32_t a)
{
    return a++;
}
