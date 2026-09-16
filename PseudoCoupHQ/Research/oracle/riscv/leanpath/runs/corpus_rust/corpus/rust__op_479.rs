// probe 479 -- binary <<
#[no_mangle]
pub fn op_479(a: u64, b: bool) -> <u64 as core::ops::Shl<bool>>::Output {
    a << b
}
