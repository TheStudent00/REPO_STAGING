// probe 999 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_999(bool a, float b)
{
    return a not_eq b;
}
