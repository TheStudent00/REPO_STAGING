// probe 517 -- binary >>
#[no_mangle]
pub fn op_517(a: f32, b: i64) -> <f32 as core::ops::Shr<i64>>::Output {
    a >> b
}
