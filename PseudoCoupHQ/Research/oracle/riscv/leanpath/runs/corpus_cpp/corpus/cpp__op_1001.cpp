// probe 1001 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_1001(bool a, bool b)
{
    return a not_eq b;
}
