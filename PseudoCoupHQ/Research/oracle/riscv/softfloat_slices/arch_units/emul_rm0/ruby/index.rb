# Every emulated operation, by name.  Generated.

require_relative 'f16_add'
require_relative 'f16_div'
require_relative 'f16_eq'
require_relative 'f16_le'
require_relative 'f16_le_quiet'
require_relative 'f16_lt'
require_relative 'f16_lt_quiet'
require_relative 'f16_mul'
require_relative 'f16_mulAdd'
require_relative 'f16_roundToInt'
require_relative 'f16_sqrt'
require_relative 'f16_sub'
require_relative 'f16_to_f32'
require_relative 'f16_to_f64'
require_relative 'f16_to_i32'
require_relative 'f16_to_i64'
require_relative 'f16_to_ui32'
require_relative 'f16_to_ui64'
require_relative 'f32_add'
require_relative 'f32_div'
require_relative 'f32_eq'
require_relative 'f32_le'
require_relative 'f32_le_quiet'
require_relative 'f32_lt'
require_relative 'f32_lt_quiet'
require_relative 'f32_mul'
require_relative 'f32_mulAdd'
require_relative 'f32_roundToInt'
require_relative 'f32_sqrt'
require_relative 'f32_sub'
require_relative 'f32_to_bf16'
require_relative 'f32_to_f16'
require_relative 'f32_to_f64'
require_relative 'f32_to_i32'
require_relative 'f32_to_i64'
require_relative 'f32_to_ui32'
require_relative 'f32_to_ui64'
require_relative 'f64_add'
require_relative 'f64_div'
require_relative 'f64_eq'
require_relative 'f64_le'
require_relative 'f64_le_quiet'
require_relative 'f64_lt'
require_relative 'f64_lt_quiet'
require_relative 'f64_mul'
require_relative 'f64_mulAdd'
require_relative 'f64_roundToInt'
require_relative 'f64_sqrt'
require_relative 'f64_sub'
require_relative 'f64_to_f16'
require_relative 'f64_to_f32'
require_relative 'f64_to_i32'
require_relative 'f64_to_i64'
require_relative 'f64_to_ui32'
require_relative 'f64_to_ui64'
require_relative 'i32_to_f16'
require_relative 'i32_to_f32'
require_relative 'i32_to_f64'
require_relative 'i64_to_f16'
require_relative 'i64_to_f32'
require_relative 'i64_to_f64'
require_relative 'ui32_to_f16'
require_relative 'ui32_to_f32'
require_relative 'ui32_to_f64'
require_relative 'ui64_to_f16'
require_relative 'ui64_to_f32'
require_relative 'ui64_to_f64'

OPS = {
  'f16_add' => method(:f16_add_rm0),
  'f16_div' => method(:f16_div_rm0),
  'f16_eq' => method(:f16_eq_rm0),
  'f16_le' => method(:f16_le_rm0),
  'f16_le_quiet' => method(:f16_le_quiet_rm0),
  'f16_lt' => method(:f16_lt_rm0),
  'f16_lt_quiet' => method(:f16_lt_quiet_rm0),
  'f16_mul' => method(:f16_mul_rm0),
  'f16_mulAdd' => method(:f16_mulAdd_rm0),
  'f16_roundToInt' => method(:f16_roundToInt_rm0),
  'f16_sqrt' => method(:f16_sqrt_rm0),
  'f16_sub' => method(:f16_sub_rm0),
  'f16_to_f32' => method(:f16_to_f32_rm0),
  'f16_to_f64' => method(:f16_to_f64_rm0),
  'f16_to_i32' => method(:f16_to_i32_rm0),
  'f16_to_i64' => method(:f16_to_i64_rm0),
  'f16_to_ui32' => method(:f16_to_ui32_rm0),
  'f16_to_ui64' => method(:f16_to_ui64_rm0),
  'f32_add' => method(:f32_add_rm0),
  'f32_div' => method(:f32_div_rm0),
  'f32_eq' => method(:f32_eq_rm0),
  'f32_le' => method(:f32_le_rm0),
  'f32_le_quiet' => method(:f32_le_quiet_rm0),
  'f32_lt' => method(:f32_lt_rm0),
  'f32_lt_quiet' => method(:f32_lt_quiet_rm0),
  'f32_mul' => method(:f32_mul_rm0),
  'f32_mulAdd' => method(:f32_mulAdd_rm0),
  'f32_roundToInt' => method(:f32_roundToInt_rm0),
  'f32_sqrt' => method(:f32_sqrt_rm0),
  'f32_sub' => method(:f32_sub_rm0),
  'f32_to_bf16' => method(:f32_to_bf16_rm0),
  'f32_to_f16' => method(:f32_to_f16_rm0),
  'f32_to_f64' => method(:f32_to_f64_rm0),
  'f32_to_i32' => method(:f32_to_i32_rm0),
  'f32_to_i64' => method(:f32_to_i64_rm0),
  'f32_to_ui32' => method(:f32_to_ui32_rm0),
  'f32_to_ui64' => method(:f32_to_ui64_rm0),
  'f64_add' => method(:f64_add_rm0),
  'f64_div' => method(:f64_div_rm0),
  'f64_eq' => method(:f64_eq_rm0),
  'f64_le' => method(:f64_le_rm0),
  'f64_le_quiet' => method(:f64_le_quiet_rm0),
  'f64_lt' => method(:f64_lt_rm0),
  'f64_lt_quiet' => method(:f64_lt_quiet_rm0),
  'f64_mul' => method(:f64_mul_rm0),
  'f64_mulAdd' => method(:f64_mulAdd_rm0),
  'f64_roundToInt' => method(:f64_roundToInt_rm0),
  'f64_sqrt' => method(:f64_sqrt_rm0),
  'f64_sub' => method(:f64_sub_rm0),
  'f64_to_f16' => method(:f64_to_f16_rm0),
  'f64_to_f32' => method(:f64_to_f32_rm0),
  'f64_to_i32' => method(:f64_to_i32_rm0),
  'f64_to_i64' => method(:f64_to_i64_rm0),
  'f64_to_ui32' => method(:f64_to_ui32_rm0),
  'f64_to_ui64' => method(:f64_to_ui64_rm0),
  'i32_to_f16' => method(:i32_to_f16_rm0),
  'i32_to_f32' => method(:i32_to_f32_rm0),
  'i32_to_f64' => method(:i32_to_f64_rm0),
  'i64_to_f16' => method(:i64_to_f16_rm0),
  'i64_to_f32' => method(:i64_to_f32_rm0),
  'i64_to_f64' => method(:i64_to_f64_rm0),
  'ui32_to_f16' => method(:ui32_to_f16_rm0),
  'ui32_to_f32' => method(:ui32_to_f32_rm0),
  'ui32_to_f64' => method(:ui32_to_f64_rm0),
  'ui64_to_f16' => method(:ui64_to_f16_rm0),
  'ui64_to_f32' => method(:ui64_to_f32_rm0),
  'ui64_to_f64' => method(:ui64_to_f64_rm0),
}.freeze
