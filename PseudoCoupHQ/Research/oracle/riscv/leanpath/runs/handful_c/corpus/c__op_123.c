/* probe 123 -- binary + */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} + (float){0})
op_123(float a, float b)
{
    return a + b;
}
