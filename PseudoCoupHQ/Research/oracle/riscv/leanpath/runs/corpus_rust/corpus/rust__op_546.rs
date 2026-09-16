// probe 546 -- binary +
#[no_mangle]
pub fn op_546(a: u64, b: i32) -> <u64 as core::ops::Add<i32>>::Output {
    a + b
}
