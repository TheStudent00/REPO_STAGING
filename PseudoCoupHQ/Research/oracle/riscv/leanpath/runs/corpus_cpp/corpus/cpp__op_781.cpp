// probe 781 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_781(bool a, int64_t b)
{
    return a <=> b;
}
