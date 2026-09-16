// probe 589 -- binary -
#[no_mangle]
pub fn op_589(a: f32, b: i64) -> <f32 as core::ops::Sub<i64>>::Output {
    a - b
}
