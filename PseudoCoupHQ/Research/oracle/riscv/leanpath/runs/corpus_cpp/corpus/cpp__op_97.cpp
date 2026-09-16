// probe 97 -- unary ...
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_97(int64_t a)
{
    return a...;
}
