#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E00672__c_regen_20875.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~(If(fpIsNaN(fpToFP(Extract(63, 0, v0))), 1, 0) | If(Or(Not(fpEQ(fpToFP(Extract(63, 0, v0)), +0.0)), fpIsNaN(fpToFP(Extract(63, 0, v0)))), 1, 0)) | If(Extract(15, 0, v1) == 0, 255, 254)))
#[no_mangle]
pub extern "C" fn emu_E00672__c_regen_20875(a: u16, b: u64, c: u64, d: f64, e: f64) -> u32
{
    (((((((0x0u32) as u32) << 8) | (((((!((((((((((!((((((((if (((d) != (d))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32) | (((if (((((d) != (d))) || ((!(((d) == ((0.0f64)))))))) { ((0x1u32) as u32) } else { ((0x0u32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32) | (((if (((((a as u32)) as u32) == ((0x0u32) as u32))) { ((0xffu32) as u32) } else { ((0xfeu32) as u32) })) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32)) as u32)
}
