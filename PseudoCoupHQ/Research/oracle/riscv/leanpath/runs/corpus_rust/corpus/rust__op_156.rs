// probe 156 -- binary &
#[no_mangle]
pub fn op_156(a: f32, b: i32) -> <f32 as core::ops::BitAnd<i32>>::Output {
    a & b
}
