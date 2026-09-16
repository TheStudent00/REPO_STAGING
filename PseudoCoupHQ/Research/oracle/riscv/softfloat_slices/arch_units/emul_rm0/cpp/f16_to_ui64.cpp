#include "sfemul.hpp"

namespace sfemul {


uint64_t f16_to_ui64_rm0(uint64_t v_arg)
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
    const uint64_t v__m30 = (uint64_t)((v_i7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a31 = (uint64_t)(v_i12 & v__m30);
    const uint32_t v__m18 = (uint32_t)((v__n17) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a19 = (uint32_t)(v__o16 & v__m18);
    const uint32_t v__sh20 = (uint32_t)((uint32_t)(v__a19) >> ((UINT32_C(0xc)) & 31));
    const uint32_t v_i33 = v__sh20;
    const uint64_t v_i34 = (uint64_t)(v_i33);
    const uint64_t v_i35 = (uint64_t)(v__a19);
    const uint64_t v__sh21 = (uint64_t)((uint64_t)(v_i35) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i36 = v__sh21;
    const bool v_i37 = ((int64_t)(v_i36) < INT64_C(0));
    const bool v_i39 = (v_i36 == UINT64_C(0x8000000000000000));
    const uint64_t v__m22 = (uint64_t)((v_i39) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__m26 = (uint64_t)((v_i37) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i38 = (uint64_t)(v_i34 + UINT64_C(0x1));
    const uint64_t v_i40 = (uint64_t)(v_i38 & UINT64_C(0x1ffffe));
    const uint64_t v__a23 = (uint64_t)(v_i40 & v__m22);
    const uint64_t v__n24 = (uint64_t)(v__m22 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a25 = (uint64_t)(v_i38 & v__n24);
    const uint64_t v_i41 = (uint64_t)(v__a23 | v__a25);
    const uint64_t v__a27 = (uint64_t)(v_i41 & v__m26);
    const uint64_t v__n28 = (uint64_t)(v__m26 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a29 = (uint64_t)(v_i34 & v__n28);
    const uint64_t v_i42 = (uint64_t)(v__a27 | v__a29);
    const bool v_i43 = (v_i42 != UINT64_C(0x0));
    const bool v_i44 = (v_i1 && v_i43);
    const uint64_t v_i47 = (uint64_t)((v_i10) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v__n32 = (v_i19 != true);
    const bool v__c33 = (v__n17 && v__n3);
    const bool v__c34 = (v__c33 && v__n32);
    const bool v__c39 = (v__c33 && v_i19);
    const bool v__c41 = (v__c39 || v_i15);
    const uint64_t v__m35 = (uint64_t)((v__c34) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a36 = (uint64_t)(v_i24 & v__m35);
    const uint64_t v__o37 = (uint64_t)(v__a31 | v__a36);
    const bool v__c42 = (v__c41 && v_i44);
    const uint64_t v__m43 = (uint64_t)((v__c42) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a44 = (uint64_t)(v_i47 & v__m43);
    const uint64_t v__o45 = (uint64_t)(v__o37 | v__a44);
    const bool v__n46 = (v_i44 != true);
    const bool v__c47 = (v__c41 && v__n46);
    const uint64_t v__m48 = (uint64_t)((v__c47) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a49 = (uint64_t)(v_i42 & v__m48);
    const uint64_t v__o50 = (uint64_t)(v__o45 | v__a49);
    return v__o50;
}

}  // namespace sfemul
