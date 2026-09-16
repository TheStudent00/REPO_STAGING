// probe 388 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_388(bool a, double b)
{
    return a | b;
}
