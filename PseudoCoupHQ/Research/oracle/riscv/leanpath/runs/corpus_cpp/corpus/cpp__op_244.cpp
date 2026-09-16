// probe 244 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_244(bool a, double b)
{
    return a / b;
}
