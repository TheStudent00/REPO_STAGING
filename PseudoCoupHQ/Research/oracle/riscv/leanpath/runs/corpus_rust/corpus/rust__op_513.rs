// probe 513 -- binary >>
#[no_mangle]
pub fn op_513(a: u64, b: f32) -> <u64 as core::ops::Shr<f32>>::Output {
    a >> b
}
