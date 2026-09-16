// probe 588 -- binary -
#[no_mangle]
pub fn op_588(a: f32, b: i32) -> <f32 as core::ops::Sub<i32>>::Output {
    a - b
}
