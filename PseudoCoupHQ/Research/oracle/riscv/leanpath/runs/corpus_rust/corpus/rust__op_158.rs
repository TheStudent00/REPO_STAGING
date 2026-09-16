// probe 158 -- binary &
#[no_mangle]
pub fn op_158(a: f32, b: u64) -> <f32 as core::ops::BitAnd<u64>>::Output {
    a & b
}
