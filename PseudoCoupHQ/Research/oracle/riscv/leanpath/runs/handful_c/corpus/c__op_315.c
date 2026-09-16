/* probe 315 -- binary || */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} || (float){0})
op_315(bool a, float b)
{
    return a || b;
}
