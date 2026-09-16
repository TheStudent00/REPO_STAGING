// probe 523 -- binary >>
#[no_mangle]
pub fn op_523(a: f64, b: i64) -> <f64 as core::ops::Shr<i64>>::Output {
    a >> b
}
