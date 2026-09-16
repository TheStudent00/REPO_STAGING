// probe 476 -- binary <<
#[no_mangle]
pub fn op_476(a: u64, b: u64) -> <u64 as core::ops::Shl<u64>>::Output {
    a << b
}
