#include "sfemul.hpp"

namespace sfemul {


uint32_t f16_to_ui32_rm0(uint64_t v_arg)
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
    const uint32_t v_i12 = (uint32_t)((v_i11) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i17 = (uint32_t)(v_i14 | UINT32_C(0x400));
    const bool v_i18 = (v_i4 < UINT32_C(0x19));
    const bool v_i19 = (v_i1 || v_i18);
    const uint8_t v_i21 = (uint8_t)(v_i4 + UINT32_C(0xe7));
    const uint32_t v_i22 = (uint32_t)(v_i21);
    const uint32_t v__sh1 = (uint32_t)((uint32_t)(v_i17) << ((v_i22) & 31));
    const uint32_t v_i23 = v__sh1;
    const bool v_i25 = (v_i4 > UINT32_C(0xd));
    const uint8_t v_i27 = (uint8_t)(v_i4 + UINT32_C(0xf3));
    const uint32_t v_i28 = (uint32_t)(v_i27);
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_i17) << ((v_i28) & 31));
    const uint32_t v_i29 = v__sh2;
    const bool v__n3 = (v_i15 != true);
    const bool v__c5 = (v_i25 && v_i19);
    const uint32_t v__m6 = (uint32_t)((v__c5) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a7 = (uint32_t)(v_i29 & v__m6);
    const bool v__n8 = (v_i25 != true);
    const bool v__c9 = (v__n3 && v_i19);
    const bool v__c10 = (v__c9 && v__n8);
    const uint32_t v__m11 = (uint32_t)((v__c10) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a12 = (uint32_t)(v_i17 & v__m11);
    const uint32_t v__o13 = (uint32_t)(v__a7 | v__a12);
    const uint32_t v__m14 = (uint32_t)((v_i15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a15 = (uint32_t)(v_i14 & v__m14);
    const uint32_t v__o16 = (uint32_t)(v__o13 | v__a15);
    const bool v__n17 = (v_i7 != true);
    const uint32_t v__m25 = (uint32_t)((v_i7) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a26 = (uint32_t)(v_i12 & v__m25);
    const uint32_t v__m18 = (uint32_t)((v__n17) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a19 = (uint32_t)(v__o16 & v__m18);
    const uint16_t v_i32 = (uint16_t)(v__a19);
    const uint16_t v_i33 = (uint16_t)(v_i32 & UINT32_C(0xfff));
    const uint32_t v_i34 = (uint32_t)(v__a19 + UINT32_C(0x800));
    const uint32_t v__sh20 = (uint32_t)((uint32_t)(v_i34) >> ((UINT32_C(0xc)) & 31));
    const uint32_t v_i35 = v__sh20;
    const bool v_i36 = (v_i33 == UINT32_C(0x800));
    const uint32_t v__m21 = (uint32_t)((v_i36) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i37 = (uint32_t)(v_i35 & UINT32_C(0xffffe));
    const uint32_t v__a22 = (uint32_t)(v_i37 & v__m21);
    const uint32_t v__n23 = (uint32_t)(v__m21 ^ UINT32_C(0xffffffff));
    const uint32_t v__a24 = (uint32_t)(v_i35 & v__n23);
    const uint32_t v_i38 = (uint32_t)(v__a22 | v__a24);
    const bool v_i39 = (v_i38 != UINT32_C(0x0));
    const bool v_i40 = (v_i1 && v_i39);
    const uint32_t v_i43 = (uint32_t)((v_i10) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v__n27 = (v_i19 != true);
    const bool v__c28 = (v__n17 && v__n3);
    const bool v__c29 = (v__c28 && v__n27);
    const bool v__c35 = (v__c28 && v_i19);
    const bool v__c36 = (v_i15 || v__c35);
    const uint32_t v__m30 = (uint32_t)((v__c29) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a31 = (uint32_t)(v_i23 & v__m30);
    const uint32_t v__o32 = (uint32_t)(v__a26 | v__a31);
    const bool v__c37 = (v__c36 && v_i40);
    const uint32_t v__m38 = (uint32_t)((v__c37) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a39 = (uint32_t)(v_i43 & v__m38);
    const uint32_t v__o40 = (uint32_t)(v__o32 | v__a39);
    const bool v__n41 = (v_i40 != true);
    const bool v__c42 = (v__c36 && v__n41);
    const uint32_t v__m43 = (uint32_t)((v__c42) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a44 = (uint32_t)(v_i38 & v__m43);
    const uint32_t v__o45 = (uint32_t)(v__o40 | v__a44);
    return v__o45;
}

}  // namespace sfemul
