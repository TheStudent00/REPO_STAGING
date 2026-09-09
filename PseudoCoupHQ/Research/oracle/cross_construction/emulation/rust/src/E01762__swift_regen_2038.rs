#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of E01762__swift_regen_2038.
// The term's layer-5 text, LITERAL:
//   If(And(Not(Or(Not(Extract(15, 7, v0) == 0), Extract(6, 0, v0) == 127)), Extract(6, 6, v0) == 0), Extract(63, 0, LShR(Concat(v1, v2), Concat(0, If(Or(Not(Extract(15, 7, v0) == 0), Extract(6, 0, v0) == 127), 63, Extract(5, 0, v0))))), v1 >> Concat(0, If(Or(Not(Extract(15, 7, v0) == 0), Extract(6, 0, v0) == 127), 63, Extract(5, 0, v0))))
#[no_mangle]
pub extern "C" fn emu_E01762__swift_regen_2038(a: u64, b: u64, c: u16) -> u64
{
    (((if (((((((((((c as u32)) >> 6) as u32) & 0x1u32)) as u32) == ((0x0u32) as u32))) && ((!(((((((((((c as u32)) >> 0) as u32) & 0x7fu32)) as u32) == ((0x7fu32) as u32))) || ((!(((((((((c as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))))))) { ((((((((((((((((b as u64)) as u128) << 64) | (((a as u64)) as u128)) as u128)) as u128).wrapping_shr(((((((((0x0u128) as u128) << 6) | (((if (((((((((((c as u32)) >> 0) as u32) & 0x7fu32)) as u32) == ((0x7fu32) as u32))) || ((!(((((((((c as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x3fu32) as u32) } else { (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u32) })) as u128)) as u128)) as u128) as u32))) as u128)) as u128) >> 0) as u64)) as u64) } else { ((((((((b as u64)) as i64)).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((if (((((((((((c as u32)) >> 0) as u32) & 0x7fu32)) as u32) == ((0x7fu32) as u32))) || ((!(((((((((c as u32)) >> 7) as u32) & 0x1ffu32)) as u32) == ((0x0u32) as u32))))))) { ((0x3fu32) as u32) } else { (((((((c as u32)) >> 0) as u32) & 0x3fu32)) as u32) })) as u64)) as u64)) as u64) as u32))) as u64)) as u64) })) as u64)
}
