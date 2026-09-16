// probe 353 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_353(bool a, bool b)
{
    return a && b;
}
