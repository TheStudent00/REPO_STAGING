// probe 481 -- binary <<
#[no_mangle]
pub fn op_481(a: f32, b: i64) -> <f32 as core::ops::Shl<i64>>::Output {
    a << b
}
