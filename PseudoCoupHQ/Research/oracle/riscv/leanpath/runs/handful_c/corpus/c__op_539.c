/* probe 539 -- binary > */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} > (bool){0})
op_539(int32_t a, bool b)
{
    return a > b;
}
