// probe 191 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_191(uint64_t a, bool b)
{
    return a * b;
}
