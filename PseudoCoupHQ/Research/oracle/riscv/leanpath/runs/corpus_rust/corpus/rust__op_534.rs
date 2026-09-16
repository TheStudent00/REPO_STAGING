// probe 534 -- binary +
#[no_mangle]
pub fn op_534(a: i32, b: i32) -> <i32 as core::ops::Add<i32>>::Output {
    a + b
}
