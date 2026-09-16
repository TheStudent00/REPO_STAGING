// probe 581 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_581(int64_t a, bool b)
{
    return a >= b;
}
