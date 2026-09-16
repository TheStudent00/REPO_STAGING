// probe 73 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_73(int64_t a)
{
    return new a;
}
