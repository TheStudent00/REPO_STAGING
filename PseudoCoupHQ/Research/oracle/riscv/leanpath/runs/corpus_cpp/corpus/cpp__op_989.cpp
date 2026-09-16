// probe 989 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_989(float a, bool b)
{
    return a not_eq b;
}
