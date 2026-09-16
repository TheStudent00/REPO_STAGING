// probe 518 -- binary >>
#[no_mangle]
pub fn op_518(a: f32, b: u64) -> <f32 as core::ops::Shr<u64>>::Output {
    a >> b
}
