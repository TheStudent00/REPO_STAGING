// probe 172 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_172(bool a, double b)
{
    return a - b;
}
