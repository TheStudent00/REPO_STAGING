// probe 985 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_985(float a, int64_t b)
{
    return a not_eq b;
}
