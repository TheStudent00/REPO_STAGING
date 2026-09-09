// probe 1 -- unary -
#[no_mangle]
pub fn emu_neg_gpr_one_64__primitive__rust(a: i64) -> <i64 as core::ops::Neg>::Output {
    -a
}
