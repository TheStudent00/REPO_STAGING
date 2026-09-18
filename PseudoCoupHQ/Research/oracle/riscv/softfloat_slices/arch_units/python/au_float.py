"""The rm0 emulations, re-exported for the arch-units. Generated."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', 'emul_rm0', 'python'))

from f16_add import f16_add_rm0
from f16_div import f16_div_rm0
from f16_eq import f16_eq_rm0
from f16_le import f16_le_rm0
from f16_le_quiet import f16_le_quiet_rm0
from f16_lt import f16_lt_rm0
from f16_lt_quiet import f16_lt_quiet_rm0
from f16_mul import f16_mul_rm0
from f16_mulAdd import f16_mulAdd_rm0
from f16_roundToInt import f16_roundToInt_rm0
from f16_sqrt import f16_sqrt_rm0
from f16_sub import f16_sub_rm0
from f16_to_f32 import f16_to_f32_rm0
from f16_to_f64 import f16_to_f64_rm0
from f16_to_i32 import f16_to_i32_rm0
from f16_to_i64 import f16_to_i64_rm0
from f16_to_ui32 import f16_to_ui32_rm0
from f16_to_ui64 import f16_to_ui64_rm0
from f32_add import f32_add_rm0
from f32_div import f32_div_rm0
from f32_eq import f32_eq_rm0
from f32_le import f32_le_rm0
from f32_le_quiet import f32_le_quiet_rm0
from f32_lt import f32_lt_rm0
from f32_lt_quiet import f32_lt_quiet_rm0
from f32_mul import f32_mul_rm0
from f32_mulAdd import f32_mulAdd_rm0
from f32_roundToInt import f32_roundToInt_rm0
from f32_sqrt import f32_sqrt_rm0
from f32_sub import f32_sub_rm0
from f32_to_bf16 import f32_to_bf16_rm0
from f32_to_f16 import f32_to_f16_rm0
from f32_to_f64 import f32_to_f64_rm0
from f32_to_i32 import f32_to_i32_rm0
from f32_to_i64 import f32_to_i64_rm0
from f32_to_ui32 import f32_to_ui32_rm0
from f32_to_ui64 import f32_to_ui64_rm0
from f64_add import f64_add_rm0
from f64_div import f64_div_rm0
from f64_eq import f64_eq_rm0
from f64_le import f64_le_rm0
from f64_le_quiet import f64_le_quiet_rm0
from f64_lt import f64_lt_rm0
from f64_lt_quiet import f64_lt_quiet_rm0
from f64_mul import f64_mul_rm0
from f64_mulAdd import f64_mulAdd_rm0
from f64_roundToInt import f64_roundToInt_rm0
from f64_sqrt import f64_sqrt_rm0
from f64_sub import f64_sub_rm0
from f64_to_f16 import f64_to_f16_rm0
from f64_to_f32 import f64_to_f32_rm0
from f64_to_i32 import f64_to_i32_rm0
from f64_to_i64 import f64_to_i64_rm0
from f64_to_ui32 import f64_to_ui32_rm0
from f64_to_ui64 import f64_to_ui64_rm0
from i32_to_f16 import i32_to_f16_rm0
from i32_to_f32 import i32_to_f32_rm0
from i32_to_f64 import i32_to_f64_rm0
from i64_to_f16 import i64_to_f16_rm0
from i64_to_f32 import i64_to_f32_rm0
from i64_to_f64 import i64_to_f64_rm0
from ui32_to_f16 import ui32_to_f16_rm0
from ui32_to_f32 import ui32_to_f32_rm0
from ui32_to_f64 import ui32_to_f64_rm0
from ui64_to_f16 import ui64_to_f16_rm0
from ui64_to_f32 import ui64_to_f32_rm0
from ui64_to_f64 import ui64_to_f64_rm0
