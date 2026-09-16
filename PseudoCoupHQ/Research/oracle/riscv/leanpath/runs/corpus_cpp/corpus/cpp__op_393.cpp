// probe 393 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_393(int32_t a, float b)
{
    return a ^ b;
}
