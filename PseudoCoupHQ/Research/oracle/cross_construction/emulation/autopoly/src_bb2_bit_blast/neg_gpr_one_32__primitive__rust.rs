// probe 0 -- unary -
#[no_mangle]
pub fn emu_neg_gpr_one_32__primitive__rust(a: i32) -> <i32 as core::ops::Neg>::Output {
    -a
}
