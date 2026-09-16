#include "sfemul.hpp"

namespace sfemul {


bool f64_lt_rm1(uint64_t v_arg, uint64_t v_arg1)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x7ff0000000000000));
    const bool v_i2 = (v_i != UINT64_C(0x7ff0000000000000));
    const uint64_t v_i3 = (uint64_t)(v_arg & UINT64_C(0xfffffffffffff));
    const bool v_i4 = (v_i3 == UINT64_C(0x0));
    const bool v_i5 = (v_i2 || v_i4);
    const uint64_t v_i7 = (uint64_t)(v_arg1 & UINT64_C(0x7ff0000000000000));
    const bool v_i8 = (v_i7 != UINT64_C(0x7ff0000000000000));
    const uint64_t v_i9 = (uint64_t)(v_arg1 & UINT64_C(0xfffffffffffff));
    const bool v_i10 = (v_i9 == UINT64_C(0x0));
    const bool v_i11 = (v_i8 || v_i10);
    const bool v__c5 = (v_i5 && v_i11);
    const uint64_t v_i13 = (uint64_t)(v_arg1 ^ v_arg);
    const bool v_i14 = ((int64_t)(v_i13) > INT64_C(-1));
    const bool v_i16 = ((int64_t)(v_arg) < INT64_C(0));
    const uint64_t v_i17 = (uint64_t)(v_arg1 | v_arg);
    const uint64_t v_i18 = (uint64_t)(v_i17 & UINT64_C(0x7fffffffffffffff));
    const bool v_i19 = (v_i18 != UINT64_C(0x0));
    const bool v_i20 = (v_i16 && v_i19);
    const bool v_i22 = (v_arg != v_arg1);
    const bool v_i23 = (v_arg < v_arg1);
    const bool v_i25 = (v_i16 != v_i23);
    const bool v_i26 = (v_i22 && v_i25);
    const bool v__a3 = (v_i26 && v_i14);
    const bool v__n1 = (v_i14 != true);
    const bool v__a2 = (v_i20 && v__n1);
    const bool v__o4 = (v__a2 || v__a3);
    const bool v__a6 = (v__o4 && v__c5);
    return v__a6;
}

}  // namespace sfemul
