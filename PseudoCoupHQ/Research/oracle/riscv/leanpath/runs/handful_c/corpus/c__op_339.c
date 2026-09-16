/* probe 339 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} && (float){0})
op_339(float a, float b)
{
    return a && b;
}
