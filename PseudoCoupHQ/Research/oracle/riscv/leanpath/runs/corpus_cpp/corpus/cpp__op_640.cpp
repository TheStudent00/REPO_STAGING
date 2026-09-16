// probe 640 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_640(bool a, double b)
{
    return a <= b;
}
