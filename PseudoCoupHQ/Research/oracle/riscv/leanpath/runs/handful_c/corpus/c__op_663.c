/* probe 663 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} < (float){0})
op_663(float a, float b)
{
    return a < b;
}
