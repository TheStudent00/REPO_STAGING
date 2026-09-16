// probe 317 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_317(bool a, bool b)
{
    return a || b;
}
