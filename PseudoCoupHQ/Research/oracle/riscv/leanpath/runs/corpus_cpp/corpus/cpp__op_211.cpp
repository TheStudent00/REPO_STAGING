// probe 211 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_211(int32_t a, int64_t b)
{
    return a / b;
}
