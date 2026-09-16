// probe 480 -- binary <<
#[no_mangle]
pub fn op_480(a: f32, b: i32) -> <f32 as core::ops::Shl<i32>>::Output {
    a << b
}
