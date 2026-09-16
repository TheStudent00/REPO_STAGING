// probe 511 -- binary >>
#[no_mangle]
pub fn op_511(a: u64, b: i64) -> <u64 as core::ops::Shr<i64>>::Output {
    a >> b
}
