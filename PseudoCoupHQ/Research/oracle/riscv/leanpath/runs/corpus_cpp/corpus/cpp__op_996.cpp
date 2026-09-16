// probe 996 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_996(bool a, int32_t b)
{
    return a not_eq b;
}
