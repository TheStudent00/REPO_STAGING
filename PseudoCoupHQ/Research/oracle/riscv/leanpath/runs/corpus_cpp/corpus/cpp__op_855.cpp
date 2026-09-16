// probe 855 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_855(bool a, float b)
{
    return a and b;
}
