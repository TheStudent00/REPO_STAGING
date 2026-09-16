// probe 505 -- binary >>
#[no_mangle]
pub fn op_505(a: i64, b: i64) -> <i64 as core::ops::Shr<i64>>::Output {
    a >> b
}
