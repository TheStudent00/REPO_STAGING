/* probe 89 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (bool){0})
op_89(bool a)
{
    return __extension__ a;
}
