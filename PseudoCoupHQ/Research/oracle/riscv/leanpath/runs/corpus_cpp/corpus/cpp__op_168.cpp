// probe 168 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_168(bool a, int32_t b)
{
    return a - b;
}
