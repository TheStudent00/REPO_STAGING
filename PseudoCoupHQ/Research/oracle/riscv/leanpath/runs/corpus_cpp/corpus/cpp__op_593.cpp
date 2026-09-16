// probe 593 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_593(float a, bool b)
{
    return a >= b;
}
