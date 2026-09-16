// probe 557 -- binary +
#[no_mangle]
pub fn op_557(a: f32, b: bool) -> <f32 as core::ops::Add<bool>>::Output {
    a + b
}
