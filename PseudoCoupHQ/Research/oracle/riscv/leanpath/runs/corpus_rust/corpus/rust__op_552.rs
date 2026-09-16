// probe 552 -- binary +
#[no_mangle]
pub fn op_552(a: f32, b: i32) -> <f32 as core::ops::Add<i32>>::Output {
    a + b
}
