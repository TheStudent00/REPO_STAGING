/* probe 85 -- unary __extension__ */
#include <stdint.h>
#include <stdbool.h>

__typeof__(__extension__ (int64_t){0})
op_85(int64_t a)
{
    return __extension__ a;
}
