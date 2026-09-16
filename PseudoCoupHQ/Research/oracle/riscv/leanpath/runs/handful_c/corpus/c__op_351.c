/* probe 351 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} && (float){0})
op_351(bool a, float b)
{
    return a && b;
}
