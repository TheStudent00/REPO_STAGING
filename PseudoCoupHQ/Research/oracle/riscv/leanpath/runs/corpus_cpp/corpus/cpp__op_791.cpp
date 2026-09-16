// probe 791 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_791(int32_t a, bool b)
{
    return a or b;
}
