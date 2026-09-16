// probe 351 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_351(bool a, float b)
{
    return a && b;
}
