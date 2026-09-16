// probe 496 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_496(bool a, double b)
{
    return a == b;
}
