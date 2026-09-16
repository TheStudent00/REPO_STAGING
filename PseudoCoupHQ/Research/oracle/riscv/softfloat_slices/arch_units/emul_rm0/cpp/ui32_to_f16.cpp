#include "sfemul.hpp"

namespace sfemul {


uint64_t ui32_to_f16_rm0(uint32_t v_arg)
{
    const bool v_i = (v_arg == UINT32_C(0x0));
    const bool v__n14 = (v_i != true);
    const uint32_t v__k1 = sf_ctlz32(v_arg);
    const uint32_t v_i2 = v__k1;
    const bool v_i3 = (v_arg < UINT32_C(0x800));
    const uint32_t v_i13 = (uint32_t)(v_i2 + UINT32_C(0xffffffef));
    const bool v_i14 = (v_arg > UINT32_C(0x7fff));
    const uint32_t v_i5 = (uint32_t)(v_i2 + UINT32_C(0xeb));
    const uint32_t v_i6 = (uint32_t)(v_i5 & UINT32_C(0xff));
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_i6) << ((UINT32_C(0xa)) & 31));
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_arg) << ((v_i6) & 31));
    const uint32_t v_i8 = v__sh3;
    const uint32_t v_i9 = (uint32_t)(v_i8 - v__sh2);
    const uint64_t v_i10 = (uint64_t)(v_i9);
    const uint64_t v_i11 = (uint64_t)(v_i10 + UINT64_C(0x6000));
    const uint32_t v_i16 = (uint32_t)(UINT32_C(0x11) - v_i2);
    const uint32_t v__sh4 = (uint32_t)((uint32_t)(v_arg) >> ((v_i16) & 31));
    const uint32_t v_i17 = v__sh4;
    const uint32_t v_i18 = (uint32_t)(v_i13 & UINT32_C(0x1f));
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(v_arg) << ((v_i18) & 31));
    const uint32_t v_i19 = v__sh5;
    const bool v_i20 = (v_i19 != UINT32_C(0x0));
    const uint32_t v_i21 = (uint32_t)((v_i20) ? 1 : 0);
    const uint32_t v_i22 = (uint32_t)(v_i17 | v_i21);
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_arg) << ((v_i13) & 31));
    const uint32_t v_i24 = v__sh6;
    const uint32_t v__m7 = (uint32_t)((v_i14) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a8 = (uint32_t)(v_i22 & v__m7);
    const bool v__n9 = (v_i14 != true);
    const uint32_t v__m10 = (uint32_t)((v__n9) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a11 = (uint32_t)(v_i24 & v__m10);
    const uint32_t v__o12 = (uint32_t)(v__a8 | v__a11);
    const bool v__n13 = (v_i3 != true);
    const bool v__c31 = (v_i3 && v__n14);
    const uint64_t v__m32 = (uint64_t)((v__c31) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a33 = (uint64_t)(v_i11 & v__m32);
    const uint32_t v__m16 = (uint32_t)((v__n13) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a17 = (uint32_t)(v__o12 & v__m16);
    const uint32_t v_i27 = (uint32_t)(UINT32_C(0x2d) - v_i2);
    const bool v_i32 = (v_i2 != UINT32_C(0x10));
    const uint8_t v_i28 = (uint8_t)(v__a17);
    const uint8_t v_i36 = (uint8_t)(v_i28 & UINT32_C(0xf));
    const bool v_i41 = (v_i36 == UINT32_C(0x8));
    const uint32_t v_i42 = (uint32_t)((v_i41) ? 1 : 0);
    const uint32_t v_i43 = (uint32_t)(v_i42 ^ UINT32_C(0xffffffff));
    const uint32_t v_i31 = (uint32_t)(v__a17 & UINT32_C(0xfff8));
    const bool v_i33 = (v_i31 > UINT32_C(0x7ff7));
    const bool v_or_cond = (v_i32 || v_i33);
    const uint32_t v_i38 = (uint32_t)(v_i31 + UINT32_C(0x8));
    const uint32_t v__sh27 = (uint32_t)((uint32_t)(v_i38) >> ((UINT32_C(0x4)) & 31));
    const uint32_t v_i39 = v__sh27;
    const uint32_t v_i44 = (uint32_t)(v_i39 & v_i43);
    const uint32_t v__a20 = (uint32_t)(v_i27 & v__m10);
    const bool v__c34 = (v__n13 && v__n9);
    const bool v__n21 = (v_or_cond != true);
    const bool v__c22 = (v_i14 && v__n21);
    const uint32_t v__m23 = (uint32_t)((v__c22) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a24 = (uint32_t)(UINT32_C(0x1d) & v__m23);
    const uint32_t v__o25 = (uint32_t)(v__a20 | v__a24);
    const uint32_t v__a26 = (uint32_t)(v__o25 & v__m16);
    const uint32_t v__sh28 = (uint32_t)((uint32_t)(v__a26) << ((UINT32_C(0xa)) & 31));
    const uint32_t v_i46 = v__sh28;
    const bool v_i45 = (v_i44 == UINT32_C(0x0));
    const uint32_t v__m29 = (uint32_t)((v_i45) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n30 = (uint32_t)(v__m29 ^ UINT32_C(0xffffffff));
    const uint32_t v_i47 = (uint32_t)(v_i46 & v__n30);
    const uint32_t v_i48 = (uint32_t)(v_i44 + v_i47);
    const uint64_t v_i49 = (uint64_t)(v_i48);
    const bool v__c39 = (v__c34 || v__c22);
    const bool v__c45 = (v_i14 && v_or_cond);
    const uint64_t v__m40 = (uint64_t)((v__c39) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a41 = (uint64_t)(v_i49 & v__m40);
    const uint64_t v__o42 = (uint64_t)(v__a33 | v__a41);
    const uint64_t v__m46 = (uint64_t)((v__c45) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a47 = (uint64_t)(UINT64_C(0x7c00) & v__m46);
    const uint64_t v__o48 = (uint64_t)(v__o42 | v__a47);
    const uint64_t v_i51 = (uint64_t)(v__o48 & UINT64_C(0xffff));
    return v_i51;
}

}  // namespace sfemul
