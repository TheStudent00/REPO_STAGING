// probe 161 -- binary &
#[no_mangle]
pub fn op_161(a: f32, b: bool) -> <f32 as core::ops::BitAnd<bool>>::Output {
    a & b
}
