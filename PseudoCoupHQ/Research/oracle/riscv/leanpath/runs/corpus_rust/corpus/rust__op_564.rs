// probe 564 -- binary +
#[no_mangle]
pub fn op_564(a: bool, b: i32) -> <bool as core::ops::Add<i32>>::Output {
    a + b
}
