// probe 539 -- binary +
#[no_mangle]
pub fn op_539(a: i32, b: bool) -> <i32 as core::ops::Add<bool>>::Output {
    a + b
}
