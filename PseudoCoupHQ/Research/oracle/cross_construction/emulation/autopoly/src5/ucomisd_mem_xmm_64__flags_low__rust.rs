#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of ucomisd_mem_xmm_64__flags_low__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(v0))
#[no_mangle]
pub extern "C" fn emu_ucomisd_mem_xmm_64__flags_low__rust(a: u64) -> u64
{
    ((((f64::from_bits(((a as u64)) as u64)).to_bits() as u64)) as u64)
}
