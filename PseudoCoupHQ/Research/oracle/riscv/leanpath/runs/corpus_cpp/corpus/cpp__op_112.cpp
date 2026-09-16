// probe 112 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_112(int64_t a, double b)
{
    return a + b;
}
