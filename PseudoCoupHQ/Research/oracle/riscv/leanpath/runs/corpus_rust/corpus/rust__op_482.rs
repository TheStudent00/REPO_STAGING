// probe 482 -- binary <<
#[no_mangle]
pub fn op_482(a: f32, b: u64) -> <f32 as core::ops::Shl<u64>>::Output {
    a << b
}
