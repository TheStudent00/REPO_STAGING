// probe 507 -- binary >>
#[no_mangle]
pub fn op_507(a: i64, b: f32) -> <i64 as core::ops::Shr<f32>>::Output {
    a >> b
}
