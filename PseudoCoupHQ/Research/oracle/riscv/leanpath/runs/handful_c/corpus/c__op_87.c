/* probe 87 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (float){0})
op_87(float a)
{
    return __extension__ a;
}
