/* probe 659 -- binary < */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} < (bool){0})
op_659(uint64_t a, bool b)
{
    return a < b;
}
