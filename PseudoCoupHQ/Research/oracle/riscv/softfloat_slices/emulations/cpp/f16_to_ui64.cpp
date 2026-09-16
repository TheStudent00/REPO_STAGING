#include "sfemul.hpp"

namespace sfemul {


uint64_t f16_to_ui64_rm1(uint64_t v_arg)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x8000));
    const bool v_i1 = (v_i != UINT64_C(0x0));
    const uint64_t v_i2 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0xa)) & 63));
    const uint8_t v_i3 = (uint8_t)(v_i2);
    const uint8_t v_i4 = (uint8_t)(v_i3 & UINT32_C(0x1f));
    const uint16_t v_i5 = (uint16_t)(v_arg);
    const uint16_t v_i6 = (uint16_t)(v_i5 & UINT32_C(0x3ff));
    const bool v_i7 = (v_i4 == UINT32_C(0x1f));
    const uint32_t v_i14 = (uint32_t)(v_i6);
    const bool v_i9 = (v_i6 != UINT32_C(0x0));
    const bool v_i15 = (v_i4 == UINT32_C(0x0));
    const bool v_i10 = (v_i1 != true);
    const bool v_i11 = (v_i9 || v_i10);
    const uint64_t v_i12 = (uint64_t)((v_i11) ? ~(uint64_t)0 : (uint64_t)0);
    const uint32_t v_i17 = (uint32_t)(v_i14 | UINT32_C(0x400));
    const bool v_i18 = (v_i4 < UINT32_C(0x19));
    const bool v_i19 = (v_i1 || v_i18);
    const uint8_t v_i21 = (uint8_t)(v_i4 + UINT32_C(0xe7));
    const uint32_t v_i22 = (uint32_t)(v_i21);
    const uint32_t v__sh1 = (uint32_t)((uint32_t)(v_i17) << ((v_i22) & 31));
    const uint32_t v_i23 = v__sh1;
    const uint64_t v_i24 = (uint64_t)(v_i23);
    const bool v_i26 = (v_i4 > UINT32_C(0xd));
    const uint8_t v_i28 = (uint8_t)(v_i4 + UINT32_C(0xf3));
    const uint32_t v_i29 = (uint32_t)(v_i28);
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_i17) << ((v_i29) & 31));
    const uint32_t v_i30 = v__sh2;
    const bool v__n3 = (v_i15 != true);
    const bool v__c5 = (v_i26 && v_i19);
    const uint32_t v__m6 = (uint32_t)((v__c5) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a7 = (uint32_t)(v_i30 & v__m6);
    const bool v__n8 = (v_i26 != true);
    const bool v__c9 = (v__n3 && v__n8);
    const uint32_t v__m11 = (uint32_t)((v__c9) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a12 = (uint32_t)(v_i17 & v__m11);
    const uint32_t v__o13 = (uint32_t)(v__a7 | v__a12);
    const uint32_t v__m14 = (uint32_t)((v_i15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a15 = (uint32_t)(v_i14 & v__m14);
    const uint32_t v__o16 = (uint32_t)(v__o13 | v__a15);
    const bool v__n17 = (v_i7 != true);
    const uint64_t v__m22 = (uint64_t)((v_i7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a23 = (uint64_t)(v_i12 & v__m22);
    const uint32_t v__m18 = (uint32_t)((v__n17) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a19 = (uint32_t)(v__o16 & v__m18);
    const uint32_t v__sh20 = (uint32_t)((uint32_t)(v__a19) >> ((UINT32_C(0xc)) & 31));
    const uint32_t v_i33 = v__sh20;
    const uint64_t v_i34 = (uint64_t)(v_i33);
    const uint64_t v_i35 = (uint64_t)(v__a19);
    const uint64_t v__sh21 = (uint64_t)((uint64_t)(v_i35) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i36 = v__sh21;
    const uint64_t v_i38 = (uint64_t)(v_i36 | v_i34);
    const bool v_i39 = (v_i38 == UINT64_C(0x0));
    const bool v_i40 = (v__a19 > UINT32_C(0xfff));
    const bool v_or_cond = (v_i39 || v_i40);
    const bool v__n36 = (v_or_cond != true);
    const bool v__n24 = (v_i19 != true);
    const bool v__c25 = (v__n17 && v__n3);
    const bool v__c26 = (v__c25 && v__n24);
    const bool v__c32 = (v__c25 && v_i19);
    const bool v__c34 = (v__c32 || v_i15);
    const uint64_t v__m27 = (uint64_t)((v__c26) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a28 = (uint64_t)(v_i24 & v__m27);
    const uint64_t v__o29 = (uint64_t)(v__a23 | v__a28);
    const bool v__c35 = (v_i10 && v__c34);
    const bool v__c37 = (v_i1 && v__c34);
    const bool v__c38 = (v__c37 && v__n36);
    const bool v__c39 = (v__c35 || v__c38);
    const uint64_t v__m40 = (uint64_t)((v__c39) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a41 = (uint64_t)(v_i34 & v__m40);
    const uint64_t v__o42 = (uint64_t)(v__o29 | v__a41);
    return v__o42;
}

}  // namespace sfemul
