// probe 971 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_971(int32_t a, bool b)
{
    return a not_eq b;
}
