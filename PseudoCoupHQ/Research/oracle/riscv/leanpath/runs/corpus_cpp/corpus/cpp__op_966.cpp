// probe 966 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_966(int32_t a, int32_t b)
{
    return a not_eq b;
}
