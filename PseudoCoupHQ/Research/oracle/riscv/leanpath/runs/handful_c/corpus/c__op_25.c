/* probe 25 -- unary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__(*(int64_t){0})
op_25(int64_t a)
{
    return *a;
}
