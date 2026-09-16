// probe 495 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_495(bool a, float b)
{
    return a == b;
}
