// probe 485 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_485(float a, bool b)
{
    return a == b;
}
