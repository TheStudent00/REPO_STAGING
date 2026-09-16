// probe 981 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_981(uint64_t a, float b)
{
    return a not_eq b;
}
