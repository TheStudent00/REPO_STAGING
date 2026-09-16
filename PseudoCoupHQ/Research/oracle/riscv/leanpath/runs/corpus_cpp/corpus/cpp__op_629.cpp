// probe 629 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_629(float a, bool b)
{
    return a <= b;
}
