// probe 574 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_574(int32_t a, double b)
{
    return a >= b;
}
