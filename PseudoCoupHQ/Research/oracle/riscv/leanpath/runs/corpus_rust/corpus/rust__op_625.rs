// probe 625 -- binary *
#[no_mangle]
pub fn op_625(a: f32, b: i64) -> <f32 as core::ops::Mul<i64>>::Output {
    a * b
}
