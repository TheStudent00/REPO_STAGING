#include "sfemul.h"


uint64_t f16_roundToInt_rm1(uint64_t v_arg, bool v_arg1)
{
    const uint16_t v_i = (uint16_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_arg);
    const uint32_t v_i3 = (uint32_t)((uint32_t)(v_i2) >> ((UINT32_C(0xa)) & 31));
    const uint32_t v_i4 = (uint32_t)(v_i3 & UINT32_C(0x1f));
    const uint32_t v_i14 = (uint32_t)(v_i2 & UINT32_C(0x3ff));
    const bool v_i15 = (v_i14 == UINT32_C(0x0));
    const bool v_i5 = (v_i4 < UINT32_C(0xf));
    const bool v_i11 = (v_i4 > UINT32_C(0x18));
    const uint64_t v_i7 = (uint64_t)(v_arg & UINT64_C(0x7fff));
    const bool v_i8 = (v_i7 == UINT64_C(0x0));
    const uint16_t v__m1 = (uint16_t)((v_i8) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v_i9 = (uint16_t)(v_i & UINT32_C(0x8000));
    const uint16_t v__a2 = (uint16_t)(v_i & v__m1);
    const uint16_t v__n3 = (uint16_t)(v__m1 ^ UINT32_C(0xffff));
    const uint16_t v__a4 = (uint16_t)(v_i9 & v__n3);
    const uint16_t v_spec_select = (uint16_t)(v__a2 | v__a4);
    const bool v_i13 = (v_i4 != UINT32_C(0x1f));
    const bool v_i16 = (v_i15 || v_i13);
    const uint16_t v__m5 = (uint16_t)((v_i16) ? ~(uint16_t)0 : (uint16_t)0);
    const uint32_t v_i18 = (uint32_t)(UINT32_C(0x19) - v_i4);
    const uint32_t v__sh9 = (uint32_t)((uint32_t)(UINT32_C(0xffff)) << ((v_i18) & 31));
    const uint32_t v_i19 = v__sh9;
    const uint16_t v_i20 = (uint16_t)(v_i19);
    const uint16_t v_i21 = (uint16_t)(v_i & v_i20);
    const uint16_t v__a6 = (uint16_t)(v_i & v__m5);
    const uint16_t v__n7 = (uint16_t)(v__m5 ^ UINT32_C(0xffff));
    const uint16_t v__a8 = (uint16_t)(UINT32_C(0x7e00) & v__n7);
    const uint16_t v_spec_select4 = (uint16_t)(v__a6 | v__a8);
    const bool v__n10 = (v_i11 != true);
    const bool v__n11 = (v_i5 != true);
    const bool v__c12 = (v__n10 && v__n11);
    const uint16_t v__m13 = (uint16_t)((v__c12) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a14 = (uint16_t)(v_i21 & v__m13);
    const uint16_t v__m15 = (uint16_t)((v_i5) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a16 = (uint16_t)(v_spec_select & v__m15);
    const uint16_t v__o17 = (uint16_t)(v__a14 | v__a16);
    const uint16_t v__m19 = (uint16_t)((v_i11) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a20 = (uint16_t)(v_spec_select4 & v__m19);
    const uint16_t v__o21 = (uint16_t)(v__o17 | v__a20);
    const uint64_t v_i23 = (uint64_t)(v__o21);
    return v_i23;
}
