/* probe 669 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((double){0} < (float){0})
op_669(double a, float b)
{
    return a < b;
}
