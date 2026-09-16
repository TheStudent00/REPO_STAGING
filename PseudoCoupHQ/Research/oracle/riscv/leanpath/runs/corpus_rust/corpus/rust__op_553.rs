// probe 553 -- binary +
#[no_mangle]
pub fn op_553(a: f32, b: i64) -> <f32 as core::ops::Add<i64>>::Output {
    a + b
}
