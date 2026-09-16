// probe 207 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_207(bool a, float b)
{
    return a * b;
}
