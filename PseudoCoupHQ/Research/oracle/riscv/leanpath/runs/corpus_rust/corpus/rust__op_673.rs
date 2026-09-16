// probe 673 -- binary /
#[no_mangle]
pub fn op_673(a: bool, b: i64) -> <bool as core::ops::Div<i64>>::Output {
    a / b
}
