// probe 173 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_173(bool a, bool b)
{
    return a - b;
}
