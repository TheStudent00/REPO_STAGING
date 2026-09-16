//! The eight LLVM intrinsics the flattened slices use, plus the three
//! don't-care pins, written once for rust and reused by every operation.
//!
//! ctlz      BUILT-IN: `leading_zeros()` returns the bit width for 0, which is
//!           exactly LLVM's ctlz with is_zero_poison=false, so the edge case
//!           matches and the built-in is used.
//! abs       BUILT-IN: `wrapping_abs()` on the signed view returns INT_MIN for
//!           INT_MIN, which is LLVM's llvm.abs with is_int_min_poison=false.
//!           `abs()` would panic, so it is not used.
//! usub.sat  BUILT-IN: `saturating_sub()` on unsigned is exactly llvm.usub.sat.
//! fshl      WRITTEN OUT.  rust has no stable funnel shift; `rotate_left` is
//!           only the a == b case.
//! udiv      WRITTEN OUT with a zero guard: rust panics on divide by zero.
//!
//! Shifts in the emitted bodies use `wrapping_shl` / `wrapping_shr`, whose
//! shift amount is taken modulo the bit width - the same pin the C, C++ and
//! go emitters make explicit with `& (W-1)`.
#![allow(dead_code)]

// ------------------------------------------------------------ intrinsics --

#[inline(always)]
pub fn sf_ctlz_u32(x: u32) -> u32 { x.leading_zeros() }

#[inline(always)]
pub fn sf_ctlz_u64(x: u64) -> u64 { x.leading_zeros() as u64 }

#[inline(always)]
pub fn sf_ctlz_u16(x: u16) -> u16 { x.leading_zeros() as u16 }

#[inline(always)]
pub fn sf_abs_u16(x: u16) -> u16 { (x as i16).wrapping_abs() as u16 }

#[inline(always)]
pub fn sf_abs_u32(x: u32) -> u32 { (x as i32).wrapping_abs() as u32 }

#[inline(always)]
pub fn sf_abs_u64(x: u64) -> u64 { (x as i64).wrapping_abs() as u64 }

#[inline(always)]
pub fn sf_usubsat_u8(a: u8, b: u8) -> u8 { a.saturating_sub(b) }

#[inline(always)]
pub fn sf_usubsat_u16(a: u16, b: u16) -> u16 { a.saturating_sub(b) }

#[inline(always)]
pub fn sf_usubsat_u32(a: u32, b: u32) -> u32 { a.saturating_sub(b) }

#[inline(always)]
pub fn sf_fshl_u64(a: u64, b: u64, c: u64) -> u64 {
    let s = (c & 63) as u32;
    if s == 0 { a } else { (a << s) | (b >> (64 - s)) }
}

#[inline(always)]
pub fn sf_fshl_u32(a: u32, b: u32, c: u32) -> u32 {
    let s = (c & 31) as u32;
    if s == 0 { a } else { (a << s) | (b >> (32 - s)) }
}

// -------------------------------------------------------- pinned poison --

#[inline(always)]
pub fn sf_udiv_u32(a: u32, b: u32) -> u32 { if b == 0 { 0 } else { a / b } }

#[inline(always)]
pub fn sf_udiv_u64(a: u64, b: u64) -> u64 { if b == 0 { 0 } else { a / b } }

#[inline(always)]
pub fn sf_udiv_u128(a: u128, b: u128) -> u128 {
    if b == 0 { 0 } else { a / b }
}
