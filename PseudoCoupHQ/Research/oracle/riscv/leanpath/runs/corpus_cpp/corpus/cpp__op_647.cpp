// probe 647 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_647(int32_t a, bool b)
{
    return a < b;
}
