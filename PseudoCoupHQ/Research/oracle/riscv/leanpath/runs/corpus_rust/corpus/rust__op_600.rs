// probe 600 -- binary -
#[no_mangle]
pub fn op_600(a: bool, b: i32) -> <bool as core::ops::Sub<i32>>::Output {
    a - b
}
