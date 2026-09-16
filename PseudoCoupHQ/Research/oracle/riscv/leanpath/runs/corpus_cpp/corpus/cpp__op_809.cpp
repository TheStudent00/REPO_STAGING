// probe 809 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_809(float a, bool b)
{
    return a or b;
}
