// probe 243 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_243(bool a, float b)
{
    return a / b;
}
