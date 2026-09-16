// probe 659 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_659(uint64_t a, bool b)
{
    return a < b;
}
