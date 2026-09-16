// probe 461 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_461(bool a, bool b)
{
    return a & b;
}
