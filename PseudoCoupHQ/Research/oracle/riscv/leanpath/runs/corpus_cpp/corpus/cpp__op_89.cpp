// probe 89 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_89(bool a)
{
    return a++;
}
