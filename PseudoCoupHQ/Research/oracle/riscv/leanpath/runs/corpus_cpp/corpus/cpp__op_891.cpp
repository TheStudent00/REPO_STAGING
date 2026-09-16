// probe 891 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_891(bool a, float b)
{
    return a bitor b;
}
