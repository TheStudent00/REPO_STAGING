// probe 570 -- binary -
#[no_mangle]
pub fn op_570(a: i32, b: i32) -> <i32 as core::ops::Sub<i32>>::Output {
    a - b
}
