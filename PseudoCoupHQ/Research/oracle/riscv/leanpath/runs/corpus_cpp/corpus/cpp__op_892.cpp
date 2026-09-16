// probe 892 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_892(bool a, double b)
{
    return a bitor b;
}
