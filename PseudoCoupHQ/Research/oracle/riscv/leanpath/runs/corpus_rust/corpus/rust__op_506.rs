// probe 506 -- binary >>
#[no_mangle]
pub fn op_506(a: i64, b: u64) -> <i64 as core::ops::Shr<u64>>::Output {
    a >> b
}
