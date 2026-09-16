// probe 665 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_665(float a, bool b)
{
    return a < b;
}
