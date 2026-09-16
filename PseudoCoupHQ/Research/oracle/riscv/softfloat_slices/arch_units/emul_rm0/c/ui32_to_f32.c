#include "sfemul.h"


uint64_t ui32_to_f32_rm0(uint32_t v_arg)
{
    const bool v_i = (v_arg == UINT32_C(0x0));
    const bool v__n25 = (v_i != true);
    const uint32_t v__m26 = (uint32_t)((v__n25) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v_i2 = ((int32_t)(v_arg) > INT32_C(-1));
    const uint32_t v__k1 = sf_ctlz32(v_arg);
    const uint32_t v_i17 = v__k1;
    const uint8_t v_i18 = (uint8_t)(v_i17);
    const uint8_t v_i19 = (uint8_t)(v_i18 + UINT32_C(0xff));
    const uint32_t v_i20 = (uint32_t)(v_i19);
    const uint16_t v_i21 = (uint16_t)(v_i19);
    const uint16_t v_i22 = (uint16_t)(UINT32_C(0x9c) - v_i21);
    const bool v_i23 = (v_arg < UINT32_C(0x1000000));
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_arg) >> ((UINT32_C(0x1)) & 31));
    const uint32_t v_i4 = (uint32_t)(v_arg & UINT32_C(0x1));
    const uint32_t v_i5 = (uint32_t)(v__sh2 + UINT32_C(0x40));
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_i5) >> ((UINT32_C(0x7)) & 31));
    const uint32_t v__masked = (uint32_t)(v__sh2 & UINT32_C(0x7f));
    const uint32_t v_i7 = (uint32_t)(v__masked | v_i4);
    const bool v_i9 = (v_i7 == UINT32_C(0x40));
    const uint32_t v_i10 = (uint32_t)((v_i9) ? 1 : 0);
    const uint32_t v_i11 = (uint32_t)(v_i10 ^ UINT32_C(0xffffffff));
    const uint32_t v_i12 = (uint32_t)(v__sh3 & v_i11);
    const bool v_i13 = (v_i12 == UINT32_C(0x0));
    const uint32_t v__m4 = (uint32_t)((v_i13) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n5 = (uint32_t)(v__m4 ^ UINT32_C(0xffffffff));
    const uint32_t v_i14 = (uint32_t)(UINT32_C(0x4e800000) & v__n5);
    const uint32_t v_i15 = (uint32_t)(v_i12 + v_i14);
    const uint32_t v_i25 = (uint32_t)(v_i22);
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_i25) << ((UINT32_C(0x17)) & 31));
    const uint32_t v_i26 = v__sh6;
    const uint32_t v_i27 = (uint32_t)(v_i20 + UINT32_C(0xfffffff9));
    const uint32_t v__sh7 = (uint32_t)((uint32_t)(v_arg) << ((v_i27) & 31));
    const uint32_t v_i28 = v__sh7;
    const uint32_t v_i29 = (uint32_t)(v_i28 + v_i26);
    const uint32_t v__sh8 = (uint32_t)((uint32_t)(v_arg) << ((v_i20) & 31));
    const uint32_t v_i30 = v__sh8;
    const uint32_t v_i31 = (uint32_t)(v_i30 + UINT32_C(0x40));
    const uint32_t v__sh9 = (uint32_t)((uint32_t)(v_i31) >> ((UINT32_C(0x7)) & 31));
    const uint32_t v_i33 = (uint32_t)(v_i30 & UINT32_C(0x7f));
    const bool v_i35 = (v_i33 == UINT32_C(0x40));
    const uint32_t v_i36 = (uint32_t)((v_i35) ? 1 : 0);
    const uint32_t v_i37 = (uint32_t)(v_i36 ^ UINT32_C(0xffffffff));
    const uint32_t v_i38 = (uint32_t)(v__sh9 & v_i37);
    const bool v_i39 = (v_i38 == UINT32_C(0x0));
    const uint32_t v__m11 = (uint32_t)((v_i39) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n12 = (uint32_t)(v__m11 ^ UINT32_C(0xffffffff));
    const uint32_t v_i42 = (uint32_t)(v_i26 & v__n12);
    const uint32_t v_i43 = (uint32_t)(v_i38 + v_i42);
    const bool v__n13 = (v_i2 != true);
    const uint32_t v__m14 = (uint32_t)((v__n13) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a15 = (uint32_t)(v_i15 & v__m14);
    const uint32_t v__m17 = (uint32_t)((v_i23) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a18 = (uint32_t)(v_i29 & v__m17);
    const uint32_t v__o19 = (uint32_t)(v__a15 | v__a18);
    const bool v__n20 = (v_i23 != true);
    const bool v__c21 = (v_i2 && v__n20);
    const uint32_t v__m22 = (uint32_t)((v__c21) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a23 = (uint32_t)(v_i43 & v__m22);
    const uint32_t v__o24 = (uint32_t)(v__o19 | v__a23);
    const uint32_t v__a27 = (uint32_t)(v__o24 & v__m26);
    const uint64_t v_i44 = (uint64_t)(v__a27);
    return v_i44;
}
