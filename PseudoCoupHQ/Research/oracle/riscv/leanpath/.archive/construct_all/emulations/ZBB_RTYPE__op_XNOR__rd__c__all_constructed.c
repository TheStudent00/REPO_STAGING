/* task t4 emulation -- rendered by render_general.py, one named
   intermediate per node of the term of ZBB_RTYPE__op_XNOR__rd__c__all_constructed.  The term's text, LITERAL:
    */
#include <stdint.h>

uint64_t
emu_ZBB_RTYPE__op_XNOR__rd__c__all_constructed(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)a) ^ (uint64_t)((uint64_t)b));
    uint64_t v1 = (uint64_t)(~(uint64_t)(v0));
    return (uint64_t)(v1);
}
