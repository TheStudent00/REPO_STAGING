// probe 593 -- binary -
#[no_mangle]
pub fn op_593(a: f32, b: bool) -> <f32 as core::ops::Sub<bool>>::Output {
    a - b
}
