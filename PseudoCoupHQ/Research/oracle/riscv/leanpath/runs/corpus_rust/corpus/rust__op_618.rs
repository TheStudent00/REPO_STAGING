// probe 618 -- binary *
#[no_mangle]
pub fn op_618(a: u64, b: i32) -> <u64 as core::ops::Mul<i32>>::Output {
    a * b
}
