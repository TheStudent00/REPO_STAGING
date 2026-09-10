#include <stdint.h>
#include <stdbool.h>
#include <string.h>

static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1)) */

uint64_t
emu_add_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) + (uint32_t)((uint32_t)b)))));
}

/* probe 138 -- binary - */

__typeof__((int32_t){0} - (int32_t){0})
emu_sub_gpr_gpr_32__primitive__c(int32_t a, int32_t b)
{
    return a - b;
}

/* probe 174 -- binary * */

__typeof__((int32_t){0} * (int32_t){0})
emu_imul_gpr_gpr_32__primitive__c(int32_t a, int32_t b)
{
    return a * b;
}

/* probe 181 -- binary * */

__typeof__((int64_t){0} * (int64_t){0})
emu_imul_gpr_gpr_64__primitive__c(int64_t a, int64_t b)
{
    return a * b;
}

/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00310__go_op_176.  The term's layer-5 text, LITERAL:
   ~(~(v0 << Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(63, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1))) */

uint64_t
emu_E00310__go_op_176(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 7) & UINT64_C(0x1ffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)))) * (uint64_t)(UINT64_C(0xffffffffffffffff)))))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)a) << (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x3f)))))))))))));
}

/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of E00316__go_op_218.  The term's layer-5 text, LITERAL:
   ~(~LShR(v0, Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(63, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1))) */

uint64_t
emu_E00316__go_op_218(uint64_t a, uint64_t b)
{
    return (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x3f))))))))) | (uint64_t)((uint64_t)(~(uint64_t)((uint64_t)((uint64_t)(((((((uint32_t)(UINT32_C(0x40)) <= (uint32_t)(((uint32_t)((uint64_t)b >> 0) & UINT32_C(0x7f))))) || ((!(((uint64_t)(((uint64_t)((uint64_t)b >> 7) & UINT64_C(0x1ffffffffffffff))) == (uint64_t)(UINT64_C(0x0)))))))) ? (uint64_t)(UINT64_C(0x0)) : (uint64_t)(UINT64_C(0x1)))) * (uint64_t)(UINT64_C(0xffffffffffffffff))))))))));
}

/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of addsd_xmm_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1))) */

double
emu_addsd_xmm_xmm_64__reg_xmm0__c(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)((a) + (b))))));
}

/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of mulsd_xmm_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) * fpToFP(Extract(63, 0, v1))) */

double
emu_mulsd_xmm_xmm_64__reg_xmm0__c(double a, double b)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)((a) * (b))))));
}

int32_t
f1_i32_add_sub(int32_t a, int32_t b, int32_t c)
{
    int32_t hub_t0 = (int32_t)((uint32_t)(emu_add_gpr_gpr_32__reg_rdi__c((uint32_t)(a), (uint32_t)(b))));
    int32_t hub_t1 = (int32_t)((uint32_t)(emu_sub_gpr_gpr_32__primitive__c((int32_t)(hub_t0), (int32_t)(c))));
    return hub_t1;
}

int32_t
f2_i32_add_mul(int32_t a, int32_t b, int32_t c)
{
    int32_t hub_t0 = (int32_t)((uint32_t)(emu_add_gpr_gpr_32__reg_rdi__c((uint32_t)(a), (uint32_t)(b))));
    int32_t hub_t1 = (int32_t)((uint32_t)(emu_imul_gpr_gpr_32__primitive__c((int32_t)(hub_t0), (int32_t)(c))));
    return hub_t1;
}

int64_t
f4_i64_mul(int64_t a, int64_t b)
{
    int64_t hub_t0 = (int64_t)((uint64_t)(emu_imul_gpr_gpr_64__primitive__c((int64_t)(a), (int64_t)(b))));
    return hub_t0;
}

uint64_t
f5_u64_shift(uint64_t a, uint64_t n)
{
    uint64_t hub_t0 = (uint64_t)((uint64_t)(emu_E00310__go_op_176((uint64_t)(a), (uint64_t)(n))));
    uint64_t hub_t1 = (uint64_t)((uint64_t)(emu_E00316__go_op_218((uint64_t)(hub_t0), (uint64_t)(n))));
    return hub_t1;
}

double
f7_f64_add_mul(double a, double b, double c)
{
    double hub_t0 = (double)(emu_addsd_xmm_xmm_64__reg_xmm0__c((double)(a), (double)(b)));
    double hub_t1 = (double)(emu_mulsd_xmm_xmm_64__reg_xmm0__c((double)(hub_t0), (double)(c)));
    return hub_t1;
}
