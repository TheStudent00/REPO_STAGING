#include "sfemul.h"


bool f16_eq_rm1(uint64_t v_arg, uint64_t v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_arg1);
    const uint32_t v_i3 = (uint32_t)(v_i & UINT32_C(0x7c00));
    const bool v_i4 = (v_i3 != UINT32_C(0x7c00));
    const uint32_t v_i5 = (uint32_t)(v_i & UINT32_C(0x3ff));
    const bool v_i6 = (v_i5 == UINT32_C(0x0));
    const bool v_i7 = (v_i4 || v_i6);
    const uint32_t v_i9 = (uint32_t)(v_i2 & UINT32_C(0x7c00));
    const bool v_i10 = (v_i9 != UINT32_C(0x7c00));
    const uint32_t v_i11 = (uint32_t)(v_i2 & UINT32_C(0x3ff));
    const bool v_i12 = (v_i11 == UINT32_C(0x0));
    const bool v_i13 = (v_i10 || v_i12);
    const bool v__c1 = (v_i7 && v_i13);
    const uint32_t v_i15 = (uint32_t)(v_i2 ^ v_i);
    const uint32_t v_i18 = (uint32_t)(v_i2 | v_i);
    const uint32_t v_i16 = (uint32_t)(v_i15 & UINT32_C(0xffff));
    const bool v_i17 = (v_i16 == UINT32_C(0x0));
    const uint32_t v_i19 = (uint32_t)(v_i18 & UINT32_C(0x7fff));
    const bool v_i20 = (v_i19 == UINT32_C(0x0));
    const bool v_i21 = (v_i17 || v_i20);
    const bool v__a2 = (v_i21 && v__c1);
    return v__a2;
}
