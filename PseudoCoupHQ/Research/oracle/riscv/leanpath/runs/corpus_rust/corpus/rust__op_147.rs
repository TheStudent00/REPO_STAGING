// probe 147 -- binary &
#[no_mangle]
pub fn op_147(a: i64, b: f32) -> <i64 as core::ops::BitAnd<f32>>::Output {
    a & b
}
