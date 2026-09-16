// probe 984 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_984(float a, int32_t b)
{
    return a not_eq b;
}
