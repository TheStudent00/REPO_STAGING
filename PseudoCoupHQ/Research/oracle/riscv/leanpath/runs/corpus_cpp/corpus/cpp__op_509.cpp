// probe 509 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_509(int64_t a, bool b)
{
    return a != b;
}
