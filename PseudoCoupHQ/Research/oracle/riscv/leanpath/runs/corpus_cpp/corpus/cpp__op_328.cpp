// probe 328 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_328(int64_t a, double b)
{
    return a && b;
}
