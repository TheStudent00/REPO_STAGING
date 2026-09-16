// probe 464 -- binary <<
#[no_mangle]
pub fn op_464(a: i32, b: u64) -> <i32 as core::ops::Shl<u64>>::Output {
    a << b
}
