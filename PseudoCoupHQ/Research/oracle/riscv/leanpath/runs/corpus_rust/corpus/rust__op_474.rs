// probe 474 -- binary <<
#[no_mangle]
pub fn op_474(a: u64, b: i32) -> <u64 as core::ops::Shl<i32>>::Output {
    a << b
}
