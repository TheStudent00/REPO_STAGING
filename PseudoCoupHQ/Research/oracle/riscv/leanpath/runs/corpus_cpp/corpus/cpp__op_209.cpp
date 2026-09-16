// probe 209 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_209(bool a, bool b)
{
    return a * b;
}
