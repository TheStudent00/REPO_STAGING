// probe 245 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_245(bool a, bool b)
{
    return a / b;
}
