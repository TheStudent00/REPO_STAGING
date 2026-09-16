// probe 460 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_460(bool a, double b)
{
    return a & b;
}
