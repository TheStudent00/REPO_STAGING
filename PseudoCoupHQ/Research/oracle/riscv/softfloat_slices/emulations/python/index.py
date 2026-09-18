"""Every emulated operation, by name.  Generated."""

from f16_add import f16_add_rm1
from f16_div import f16_div_rm1
from f16_eq import f16_eq_rm1
from f16_le import f16_le_rm1
from f16_le_quiet import f16_le_quiet_rm1
from f16_lt import f16_lt_rm1
from f16_lt_quiet import f16_lt_quiet_rm1
from f16_mul import f16_mul_rm1
from f16_mulAdd import f16_mulAdd_rm1
from f16_roundToInt import f16_roundToInt_rm1
from f16_sqrt import f16_sqrt_rm1
from f16_sub import f16_sub_rm1
from f16_to_f32 import f16_to_f32_rm1
from f16_to_f64 import f16_to_f64_rm1
from f16_to_i32 import f16_to_i32_rm1
from f16_to_i64 import f16_to_i64_rm1
from f16_to_ui32 import f16_to_ui32_rm1
from f16_to_ui64 import f16_to_ui64_rm1
from f32_add import f32_add_rm1
from f32_div import f32_div_rm1
from f32_eq import f32_eq_rm1
from f32_le import f32_le_rm1
from f32_le_quiet import f32_le_quiet_rm1
from f32_lt import f32_lt_rm1
from f32_lt_quiet import f32_lt_quiet_rm1
from f32_mul import f32_mul_rm1
from f32_mulAdd import f32_mulAdd_rm1
from f32_roundToInt import f32_roundToInt_rm1
from f32_sqrt import f32_sqrt_rm1
from f32_sub import f32_sub_rm1
from f32_to_bf16 import f32_to_bf16_rm1
from f32_to_f16 import f32_to_f16_rm1
from f32_to_f64 import f32_to_f64_rm1
from f32_to_i32 import f32_to_i32_rm1
from f32_to_i64 import f32_to_i64_rm1
from f32_to_ui32 import f32_to_ui32_rm1
from f32_to_ui64 import f32_to_ui64_rm1
from f64_add import f64_add_rm1
from f64_div import f64_div_rm1
from f64_eq import f64_eq_rm1
from f64_le import f64_le_rm1
from f64_le_quiet import f64_le_quiet_rm1
from f64_lt import f64_lt_rm1
from f64_lt_quiet import f64_lt_quiet_rm1
from f64_mul import f64_mul_rm1
from f64_mulAdd import f64_mulAdd_rm1
from f64_roundToInt import f64_roundToInt_rm1
from f64_sqrt import f64_sqrt_rm1
from f64_sub import f64_sub_rm1
from f64_to_f16 import f64_to_f16_rm1
from f64_to_f32 import f64_to_f32_rm1
from f64_to_i32 import f64_to_i32_rm1
from f64_to_i64 import f64_to_i64_rm1
from f64_to_ui32 import f64_to_ui32_rm1
from f64_to_ui64 import f64_to_ui64_rm1
from i32_to_f16 import i32_to_f16_rm1
from i32_to_f32 import i32_to_f32_rm1
from i32_to_f64 import i32_to_f64_rm1
from i64_to_f16 import i64_to_f16_rm1
from i64_to_f32 import i64_to_f32_rm1
from i64_to_f64 import i64_to_f64_rm1
from ui32_to_f16 import ui32_to_f16_rm1
from ui32_to_f32 import ui32_to_f32_rm1
from ui32_to_f64 import ui32_to_f64_rm1
from ui64_to_f16 import ui64_to_f16_rm1
from ui64_to_f32 import ui64_to_f32_rm1
from ui64_to_f64 import ui64_to_f64_rm1

OPS = {
    "f16_add": f16_add_rm1,
    "f16_div": f16_div_rm1,
    "f16_eq": f16_eq_rm1,
    "f16_le": f16_le_rm1,
    "f16_le_quiet": f16_le_quiet_rm1,
    "f16_lt": f16_lt_rm1,
    "f16_lt_quiet": f16_lt_quiet_rm1,
    "f16_mul": f16_mul_rm1,
    "f16_mulAdd": f16_mulAdd_rm1,
    "f16_roundToInt": f16_roundToInt_rm1,
    "f16_sqrt": f16_sqrt_rm1,
    "f16_sub": f16_sub_rm1,
    "f16_to_f32": f16_to_f32_rm1,
    "f16_to_f64": f16_to_f64_rm1,
    "f16_to_i32": f16_to_i32_rm1,
    "f16_to_i64": f16_to_i64_rm1,
    "f16_to_ui32": f16_to_ui32_rm1,
    "f16_to_ui64": f16_to_ui64_rm1,
    "f32_add": f32_add_rm1,
    "f32_div": f32_div_rm1,
    "f32_eq": f32_eq_rm1,
    "f32_le": f32_le_rm1,
    "f32_le_quiet": f32_le_quiet_rm1,
    "f32_lt": f32_lt_rm1,
    "f32_lt_quiet": f32_lt_quiet_rm1,
    "f32_mul": f32_mul_rm1,
    "f32_mulAdd": f32_mulAdd_rm1,
    "f32_roundToInt": f32_roundToInt_rm1,
    "f32_sqrt": f32_sqrt_rm1,
    "f32_sub": f32_sub_rm1,
    "f32_to_bf16": f32_to_bf16_rm1,
    "f32_to_f16": f32_to_f16_rm1,
    "f32_to_f64": f32_to_f64_rm1,
    "f32_to_i32": f32_to_i32_rm1,
    "f32_to_i64": f32_to_i64_rm1,
    "f32_to_ui32": f32_to_ui32_rm1,
    "f32_to_ui64": f32_to_ui64_rm1,
    "f64_add": f64_add_rm1,
    "f64_div": f64_div_rm1,
    "f64_eq": f64_eq_rm1,
    "f64_le": f64_le_rm1,
    "f64_le_quiet": f64_le_quiet_rm1,
    "f64_lt": f64_lt_rm1,
    "f64_lt_quiet": f64_lt_quiet_rm1,
    "f64_mul": f64_mul_rm1,
    "f64_mulAdd": f64_mulAdd_rm1,
    "f64_roundToInt": f64_roundToInt_rm1,
    "f64_sqrt": f64_sqrt_rm1,
    "f64_sub": f64_sub_rm1,
    "f64_to_f16": f64_to_f16_rm1,
    "f64_to_f32": f64_to_f32_rm1,
    "f64_to_i32": f64_to_i32_rm1,
    "f64_to_i64": f64_to_i64_rm1,
    "f64_to_ui32": f64_to_ui32_rm1,
    "f64_to_ui64": f64_to_ui64_rm1,
    "i32_to_f16": i32_to_f16_rm1,
    "i32_to_f32": i32_to_f32_rm1,
    "i32_to_f64": i32_to_f64_rm1,
    "i64_to_f16": i64_to_f16_rm1,
    "i64_to_f32": i64_to_f32_rm1,
    "i64_to_f64": i64_to_f64_rm1,
    "ui32_to_f16": ui32_to_f16_rm1,
    "ui32_to_f32": ui32_to_f32_rm1,
    "ui32_to_f64": ui32_to_f64_rm1,
    "ui64_to_f16": ui64_to_f16_rm1,
    "ui64_to_f32": ui64_to_f32_rm1,
    "ui64_to_f64": ui64_to_f64_rm1,
}
