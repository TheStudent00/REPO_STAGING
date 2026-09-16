/* probe 86 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (uint64_t){0})
op_86(uint64_t a)
{
    return __extension__ a;
}
