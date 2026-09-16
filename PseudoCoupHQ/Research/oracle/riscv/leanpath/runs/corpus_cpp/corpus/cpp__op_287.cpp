// probe 287 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_287(int32_t a, bool b)
{
    return a || b;
}
