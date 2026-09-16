// probe 650 -- binary /
#[no_mangle]
pub fn op_650(a: i64, b: u64) -> <i64 as core::ops::Div<u64>>::Output {
    a / b
}
