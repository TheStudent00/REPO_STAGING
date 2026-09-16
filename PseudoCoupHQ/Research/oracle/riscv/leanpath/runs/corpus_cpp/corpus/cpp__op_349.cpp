// probe 349 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_349(bool a, int64_t b)
{
    return a && b;
}
