/* probe 84 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (int32_t){0})
op_84(int32_t a)
{
    return __extension__ a;
}
