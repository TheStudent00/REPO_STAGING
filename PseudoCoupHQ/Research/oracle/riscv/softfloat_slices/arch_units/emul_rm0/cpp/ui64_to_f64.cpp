#include "sfemul.hpp"

namespace sfemul {


uint64_t ui64_to_f64_rm0(uint64_t v_arg)
{
    const bool v_i = (v_arg == UINT64_C(0x0));
    const bool v__n25 = (v_i != true);
    const uint64_t v__m26 = (uint64_t)((v__n25) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i2 = ((int64_t)(v_arg) > INT64_C(-1));
    const uint64_t v__k1 = sf_ctlz64(v_arg);
    const uint64_t v_i19 = v__k1;
    const uint8_t v_i20 = (uint8_t)(v_i19);
    const uint8_t v_i21 = (uint8_t)(v_i20 + UINT32_C(0xff));
    const uint64_t v_i28 = (uint64_t)(v_i19 + UINT64_C(0xfffffff5));
    const uint64_t v_i29 = (uint64_t)(v_i28 & UINT64_C(0xffffffff));
    const uint64_t v__sh7 = (uint64_t)((uint64_t)(v_arg) << ((v_i29) & 63));
    const uint64_t v_i30 = v__sh7;
    const uint16_t v_i22 = (uint16_t)(v_i21);
    const uint16_t v_i23 = (uint16_t)(UINT32_C(0x43c) - v_i22);
    const uint64_t v_i32 = (uint64_t)(v_i21);
    const uint64_t v__sh8 = (uint64_t)((uint64_t)(v_arg) << ((v_i32) & 63));
    const uint64_t v_i33 = v__sh8;
    const bool v_i24 = (v_arg < UINT64_C(0x20000000000000));
    const uint64_t v__sh2 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0x1)) & 63));
    const uint64_t v_i4 = (uint64_t)(v_arg & UINT64_C(0x1));
    const uint64_t v_i5 = (uint64_t)(v__sh2 | v_i4);
    const uint16_t v_i6 = (uint16_t)(v_i5);
    const uint16_t v_i7 = (uint16_t)(v_i6 & UINT32_C(0x3ff));
    const uint64_t v_i8 = (uint64_t)(v__sh2 + UINT64_C(0x200));
    const uint64_t v__sh3 = (uint64_t)((uint64_t)(v_i8) >> ((UINT64_C(0xa)) & 63));
    const bool v_i11 = (v_i7 == UINT32_C(0x200));
    const uint64_t v_i12 = (uint64_t)((v_i11) ? 1 : 0);
    const uint64_t v_i13 = (uint64_t)(v_i12 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i14 = (uint64_t)(v__sh3 & v_i13);
    const bool v_i15 = (v_i14 == UINT64_C(0x0));
    const uint64_t v__m4 = (uint64_t)((v_i15) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__n5 = (uint64_t)(v__m4 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i16 = (uint64_t)(UINT64_C(0x43d0000000000000) & v__n5);
    const uint64_t v_i17 = (uint64_t)(v_i14 + v_i16);
    const uint64_t v_i26 = (uint64_t)(v_i23);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i26) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i27 = v__sh6;
    const uint64_t v_i31 = (uint64_t)(v_i30 + v_i27);
    const uint16_t v_i34 = (uint16_t)(v_i33);
    const uint16_t v_i35 = (uint16_t)(v_i34 & UINT32_C(0x3ff));
    const uint64_t v_i36 = (uint64_t)(v_i33 + UINT64_C(0x200));
    const uint64_t v__sh9 = (uint64_t)((uint64_t)(v_i36) >> ((UINT64_C(0xa)) & 63));
    const bool v_i39 = (v_i35 == UINT32_C(0x200));
    const uint64_t v_i40 = (uint64_t)((v_i39) ? 1 : 0);
    const uint64_t v_i41 = (uint64_t)(v_i40 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i42 = (uint64_t)(v__sh9 & v_i41);
    const bool v_i43 = (v_i42 == UINT64_C(0x0));
    const uint64_t v__m11 = (uint64_t)((v_i43) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__n12 = (uint64_t)(v__m11 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i46 = (uint64_t)(v_i27 & v__n12);
    const uint64_t v_i47 = (uint64_t)(v_i42 + v_i46);
    const bool v__n13 = (v_i2 != true);
    const uint64_t v__m14 = (uint64_t)((v__n13) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a15 = (uint64_t)(v_i17 & v__m14);
    const uint64_t v__m17 = (uint64_t)((v_i24) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a18 = (uint64_t)(v_i31 & v__m17);
    const uint64_t v__o19 = (uint64_t)(v__a15 | v__a18);
    const bool v__n20 = (v_i24 != true);
    const bool v__c21 = (v__n20 && v_i2);
    const uint64_t v__m22 = (uint64_t)((v__c21) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a23 = (uint64_t)(v_i47 & v__m22);
    const uint64_t v__o24 = (uint64_t)(v__o19 | v__a23);
    const uint64_t v__a27 = (uint64_t)(v__o24 & v__m26);
    return v__a27;
}

}  // namespace sfemul
