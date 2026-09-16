// probe 416 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_416(double a, uint64_t b)
{
    return a ^ b;
}
