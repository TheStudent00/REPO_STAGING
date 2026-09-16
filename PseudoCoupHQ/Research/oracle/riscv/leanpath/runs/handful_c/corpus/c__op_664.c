/* probe 664 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} < (double){0})
op_664(float a, double b)
{
    return a < b;
}
