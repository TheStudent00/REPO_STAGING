/* probe 350 -- binary && */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} && (uint64_t){0})
op_350(bool a, uint64_t b)
{
    return a && b;
}
