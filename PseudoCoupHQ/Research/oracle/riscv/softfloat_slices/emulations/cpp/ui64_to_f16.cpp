#include "sfemul.hpp"

namespace sfemul {


uint64_t ui64_to_f16_rm1(uint64_t v_arg)
{
    const bool v_i = (v_arg == UINT64_C(0x0));
    const bool v__n13 = (v_i != true);
    const uint64_t v__k1 = sf_ctlz64(v_arg);
    const uint64_t v_i2 = v__k1;
    const uint8_t v_i3 = (uint8_t)(v_i2);
    const uint64_t v_i18 = (uint64_t)(UINT64_C(0x31) - v_i2);
    const uint64_t v_i19 = (uint64_t)(v_i18 & UINT64_C(0xff));
    const bool v_i4 = (v_arg < UINT64_C(0x800));
    const uint8_t v_i15 = (uint8_t)(v_i3 + UINT32_C(0xcf));
    const uint8_t v_i6 = (uint8_t)(v_i3 + UINT32_C(0xcb));
    const uint32_t v_i7 = (uint32_t)(v_i6);
    const bool v_i16 = (v_arg > UINT64_C(0x7fff));
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_i7) << ((UINT32_C(0xa)) & 31));
    const uint32_t v_i9 = (uint32_t)(v_arg);
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_i9) << ((v_i7) & 31));
    const uint32_t v_i10 = v__sh3;
    const uint32_t v_i11 = (uint32_t)(v_i10 - v__sh2);
    const uint64_t v_i12 = (uint64_t)(v_i11);
    const uint64_t v_i13 = (uint64_t)(v_i12 + UINT64_C(0x6000));
    const uint64_t v__sh4 = (uint64_t)((uint64_t)(v_arg) >> ((v_i19) & 63));
    const uint64_t v_i20 = v__sh4;
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(UINT64_C(0xffffffffffffffff)) << ((v_i19) & 63));
    const uint64_t v_i21 = v__sh5;
    const uint64_t v_i22 = (uint64_t)(v_i21 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i23 = (uint64_t)(v_arg & v_i22);
    const bool v_i24 = (v_i23 != UINT64_C(0x0));
    const uint64_t v_i25 = (uint64_t)((v_i24) ? 1 : 0);
    const uint64_t v_i26 = (uint64_t)(v_i20 | v_i25);
    const uint32_t v_i29 = (uint32_t)(v_i15);
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_i9) << ((v_i29) & 31));
    const uint32_t v_i30 = v__sh6;
    const uint64_t v_i31 = (uint64_t)(v_i30);
    const uint64_t v__m7 = (uint64_t)((v_i16) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a8 = (uint64_t)(v_i26 & v__m7);
    const bool v__n9 = (v_i16 != true);
    const uint64_t v__m10 = (uint64_t)((v__n9) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a11 = (uint64_t)(v_i31 & v__m10);
    const uint64_t v__o12 = (uint64_t)(v__a8 | v__a11);
    const bool v__n14 = (v_i4 != true);
    const bool v__c31 = (v__n13 && v_i4);
    const uint64_t v__m32 = (uint64_t)((v__c31) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a33 = (uint64_t)(v_i13 & v__m32);
    const uint64_t v__m16 = (uint64_t)((v__n14) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a17 = (uint64_t)(v__o12 & v__m16);
    const uint32_t v__m25 = (uint32_t)((v__n14) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i34 = (uint32_t)(v__a17);
    const uint64_t v_i40 = (uint64_t)(v__a17 & UINT64_C(0x8000));
    const bool v__not = (v_i40 == UINT64_C(0x0));
    const uint32_t v__sh27 = (uint32_t)((uint32_t)(v_i34) >> ((UINT32_C(0x4)) & 31));
    const uint32_t v_i43 = v__sh27;
    const uint32_t v_i44 = (uint32_t)(v_i43 & UINT32_C(0xfff));
    const uint32_t v_i35 = (uint32_t)(int32_t)(int8_t)(v_i15);
    const uint32_t v_i36 = (uint32_t)(UINT32_C(0x1c) - v_i35);
    const bool v_i37 = (v_i15 > UINT32_C(0x1c));
    const bool v_i39 = (v_i15 == UINT32_C(0xff));
    const bool v_or_cond = (v_i39 && v__not);
    const bool v__n18 = (v_i37 != true);
    const uint32_t v__m19 = (uint32_t)((v__n18) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a20 = (uint32_t)(v_i36 & v__m19);
    const uint32_t v__m22 = (uint32_t)((v_or_cond) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a23 = (uint32_t)(UINT32_C(0x1d) & v__m22);
    const uint32_t v__o24 = (uint32_t)(v__a20 | v__a23);
    const uint32_t v__a26 = (uint32_t)(v__o24 & v__m25);
    const uint32_t v__sh28 = (uint32_t)((uint32_t)(v__a26) << ((UINT32_C(0xa)) & 31));
    const uint32_t v_i48 = v__sh28;
    const uint32_t v_i49 = (uint32_t)(v_i48 & UINT32_C(0x3fffc00));
    const bool v_i47 = (v_i44 == UINT32_C(0x0));
    const uint32_t v__m29 = (uint32_t)((v_i47) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n30 = (uint32_t)(v__m29 ^ UINT32_C(0xffffffff));
    const uint32_t v_i50 = (uint32_t)(v_i49 & v__n30);
    const uint32_t v_i51 = (uint32_t)(v_i44 + v_i50);
    const uint64_t v_i52 = (uint64_t)(v_i51);
    const bool v__c35 = (v__n14 && v__n18);
    const bool v__c36 = (v__n13 && v_or_cond);
    const bool v__c37 = (v__c36 && v__n14);
    const bool v__c39 = (v__c35 || v__c37);
    const uint64_t v__m40 = (uint64_t)((v__c39) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a41 = (uint64_t)(v_i52 & v__m40);
    const uint64_t v__o42 = (uint64_t)(v__a33 | v__a41);
    const bool v__n43 = (v_or_cond != true);
    const bool v__c44 = (v__n13 && v__n43);
    const bool v__c45 = (v__c44 && v__n14);
    const bool v__c46 = (v__c45 && v_i37);
    const uint64_t v__m47 = (uint64_t)((v__c46) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a48 = (uint64_t)(UINT64_C(0x7bff) & v__m47);
    const uint64_t v__o49 = (uint64_t)(v__o42 | v__a48);
    const uint64_t v_i54 = (uint64_t)(v__o49 & UINT64_C(0xffff));
    return v_i54;
}

}  // namespace sfemul
