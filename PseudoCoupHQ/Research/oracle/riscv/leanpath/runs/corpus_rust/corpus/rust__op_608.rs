// probe 608 -- binary *
#[no_mangle]
pub fn op_608(a: i32, b: u64) -> <i32 as core::ops::Mul<u64>>::Output {
    a * b
}
