// probe 316 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_316(bool a, double b)
{
    return a || b;
}
