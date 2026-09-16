// probe 305 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_305(float a, bool b)
{
    return a || b;
}
