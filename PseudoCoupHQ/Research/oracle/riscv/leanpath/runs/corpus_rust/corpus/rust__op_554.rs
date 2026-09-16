// probe 554 -- binary +
#[no_mangle]
pub fn op_554(a: f32, b: u64) -> <f32 as core::ops::Add<u64>>::Output {
    a + b
}
