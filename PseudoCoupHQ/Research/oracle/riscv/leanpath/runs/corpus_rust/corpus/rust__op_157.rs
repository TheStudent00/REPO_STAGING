// probe 157 -- binary &
#[no_mangle]
pub fn op_157(a: f32, b: i64) -> <f32 as core::ops::BitAnd<i64>>::Output {
    a & b
}
