// probe 649 -- binary /
#[no_mangle]
pub fn op_649(a: i64, b: i64) -> <i64 as core::ops::Div<i64>>::Output {
    a / b
}
