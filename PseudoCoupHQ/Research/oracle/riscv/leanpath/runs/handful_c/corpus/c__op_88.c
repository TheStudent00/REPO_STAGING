/* probe 88 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (double){0})
op_88(double a)
{
    return __extension__ a;
}
