// probe 626 -- binary *
#[no_mangle]
pub fn op_626(a: f32, b: u64) -> <f32 as core::ops::Mul<u64>>::Output {
    a * b
}
