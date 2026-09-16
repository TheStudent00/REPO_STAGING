// probe 161 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_161(float a, bool b)
{
    return a - b;
}
