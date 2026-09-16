// probe 323 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_323(int32_t a, bool b)
{
    return a && b;
}
