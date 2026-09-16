// probe 499 -- binary >>
#[no_mangle]
pub fn op_499(a: i32, b: i64) -> <i32 as core::ops::Shr<i64>>::Output {
    a >> b
}
