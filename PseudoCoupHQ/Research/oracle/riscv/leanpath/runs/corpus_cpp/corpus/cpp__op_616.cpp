// probe 616 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_616(int64_t a, double b)
{
    return a <= b;
}
