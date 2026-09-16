// probe 987 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_987(float a, float b)
{
    return a not_eq b;
}
