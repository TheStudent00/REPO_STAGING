// probe 893 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_893(bool a, bool b)
{
    return a bitor b;
}
