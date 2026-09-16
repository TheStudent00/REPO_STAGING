// probe 755 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_755(int32_t a, bool b)
{
    return a <=> b;
}
