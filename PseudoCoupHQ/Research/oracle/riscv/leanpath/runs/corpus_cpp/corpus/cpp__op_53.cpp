// probe 53 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_53(bool a)
{
    return ++a;
}
