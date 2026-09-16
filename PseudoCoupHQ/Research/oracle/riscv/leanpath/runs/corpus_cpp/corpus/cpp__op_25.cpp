// probe 25 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_25(int64_t a)
{
    return not a;
}
