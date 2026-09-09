#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of control__E00228__rust_op_382.
// The term's layer-5 text, LITERAL:
//   If(And(Not(fpToFP(Extract(63, 0, v0)) < fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 1, 0)
#[no_mangle]
pub extern "C" fn emu_control__E00228__rust_op_382(a: f64, b: f64) -> u8
{
    (((if ((((!(((b) < (a))))) && ((!(((((a) != (a))) || (((b) != (b))))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u8)
}
