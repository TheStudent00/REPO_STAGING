// probe 137 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_137(bool a, bool b)
{
    return a + b;
}
